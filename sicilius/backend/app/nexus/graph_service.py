import networkx as nx
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.company import Company
from app.models.person import Person
from app.models.relation import CompanyPersonRelation
from app.models.announcement import Announcement
from app.models.ocr_result import OcrResult
from app.nexus.ml.features import extract_capital, calculate_sector_entropy
from app.nexus.ml.anomaly import NexusAnomalyDetector
from uuid import UUID
import logging

logger = logging.getLogger(__name__)

class NexusGraphService:
    def __init__(self, db: Session):
        self.db = db

    def _normalize_location(self, address: str) -> str:
        """
        Simple location normalization to detect shared addresses.
        In a real scenario, this would parsing street, number, door etc.
        """
        if not address:
            return "UNKNOWN"
        # Basic cleanup: uppercase, remove excessive spaces
        cleaned = " ".join(address.upper().split())
        return cleaned

    def _mask_name(self, full_name: str) -> str:
        """
        Masks person names for KVKK compliance (e.g. 'AHMET YILMAZ' -> 'AH*** YIL***').
        Mimics the frontend's masking logic: keeps first 2 letters, masks the rest.
        """
        if not full_name:
            return ""
        
        parts = full_name.split()
        masked_parts = []
        
        for part in parts:
            if len(part) <= 2:
                masked_parts.append(part)
                continue
            
            # Mask characters after the first 2
            masked_word = part[:2] + '*' * (len(part) - 2)
            masked_parts.append(masked_word)
            
        return " ".join(masked_parts)

    def _get_node_features(self, company: Company) -> dict:
        """
        Extracts ML features for a single company using GLOBAL (Intrinsic) data.
        This ensures the AI score is consistent regardless of the current graph view.
        """
        # 1. Capital from OCR
        ocr_res = self.db.query(OcrResult).filter(OcrResult.company_id == company.id).order_by(OcrResult.created_at.desc()).first()
        capital = extract_capital(ocr_res.original_text) if ocr_res else 0.0
        
        # 2. Global Address Density (Specific to this company's address)
        density = 1
        if company.address:
            # OPTIMIZATION: Index on address is crucial here
            density = self.db.query(Company).filter(Company.address == company.address).count()

        # 3. Global Network Stats (Intrinsic Connectivity)
        # Instead of "Graph Degree" (View dependent), use "DB Degree" (Absolute truth)
        global_degree = self.db.query(CompanyPersonRelation).filter(CompanyPersonRelation.company_id == company.id).count()
        
        # 4. Partnership Structure (How many partners?)
        # This might be similar to degree but semantically distinct (In-degree vs Out-degree usually)
        # For now, simplistic total relation count serves as both.
        
        # 5. Business Complexity (Heuristic)
        # Long titles usually indicate detailed scope. Short/Generic titles might be shell.
        title_len = len(company.unvan) if company.unvan else 0
        
        # 6. Address Sector Entropy (High Risk Indicator)
        # Are neighbors at the same address in the same sector?
        address_entropy = 0.0
        if company.address:
             # Fetch 10 neighbors at same address
             neighbors = self.db.query(Company.unvan).filter(
                 Company.address == company.address,
                 Company.id != company.id
             ).limit(10).all()
             
             if neighbors:
                 titles = [company.unvan] + [n[0] for n in neighbors]
                 address_entropy = calculate_sector_entropy(titles)

        return {
            "id": str(company.id),
            "capital": capital,
            "address_density": density,
            "global_degree": global_degree,
            "title_len": title_len,
            "address_entropy": address_entropy
        }

    def analyze_company_network(self, target_company_id: UUID, depth: int = 2, limit: int = 10) -> dict:
        """
        Builds a relationship graph of Companies ONLY.
        Companies are linked if they share a Person or an Address.
        Integates Unsupervised Learning (Isolation Forest) for Anomaly Detection.
        """
        G = nx.DiGraph()
        
        visited_companies = set()
        queue = [(target_company_id, 0)]
        
        # Address map for risk analysis (Legacy/Visualization)
        address_map = {}
        
        # Feature Collection for ML
        node_features_map = {}
        
        # Track missing coordinates for background processing
        missing_coords = set()

        while queue:
            if G.number_of_nodes() >= limit:
                break

            current_id, current_depth = queue.pop(0)
            
            if current_depth >= depth:
                continue

            if current_id in visited_companies:
                continue
            visited_companies.add(current_id)

            # 1. Fetch Company
            comp = self.db.query(Company).filter(Company.id == current_id).first()
            if not comp:
                continue

            # 2. Add Node
            # Colors/Types: "company" is standard. "target" can be distinguished by ID in UI.
            G.add_node(str(comp.id), label=comp.unvan, type="company", 
                       risk_status=self._check_risk_status(comp))
            
            # Extract ML Features
            if str(comp.id) not in node_features_map:
                node_features_map[str(comp.id)] = self._get_node_features(comp)

            # Track Address for Analysis
            if comp.address:
                norm_addr = self._normalize_location(comp.address)
                if norm_addr not in address_map:
                    address_map[norm_addr] = []
                address_map[norm_addr].append(str(comp.id))

            # Stop expansion if limit reached (but make sure to add the current node first)
            
            # --- GLOBAL HEADS-UP CHECK (USER REQUEST) ---
            # Even if we don't load all nodes due to limit, we MUST know if this address is crowded.
            # Only do this for the TARGET company (depth=0) to be efficient.
            if current_depth == 0 and comp.address:
                 # We already calculated density in _get_node_features, reuse if possible or query
                 # For safety/clarity keeping explicit here as it modifies address_map
                 total_at_address = node_features_map[str(comp.id)]['address_density']
                 if total_at_address > 3:
                     # Mark this address as suspicious in the map conceptually
                     # We'll use a special key for global risks
                     address_map[f"GLOBAL_RISK::{norm_addr}"] = ["DUMMY"] * total_at_address

            remaining_nodes = limit - G.number_of_nodes()
            if remaining_nodes <= 0:
                break

            # 3. Find Neighbors via Shared Persons
            # Logic: Find Persons of Current Company -> Find Other Companies of those Persons
            # SQL:
            # SELECT cp2.company_id, p.full_name as person_name, cp1.relation_type as r1, cp2.relation_type as r2
            # FROM company_person_relation cp1
            # JOIN company_person_relation cp2 ON cp1.person_id = cp2.person_id
            # JOIN person p ON p.id = cp1.person_id
            # WHERE cp1.company_id = :current_id AND cp2.company_id != :current_id
            
            # Using SQLAlchemy ORM:
            alias_cpr1 = CompanyPersonRelation
            alias_cpr2 = CompanyPersonRelation # Need alias? No, can use same model if careful or aliased
            from sqlalchemy.orm import aliased
            CPR2 = aliased(CompanyPersonRelation) 
            
            # We want to find distinct other companies.
            # Fetching raw tuples to avoid object overhead and N+1
            shared_person_results = (
                self.db.query(CPR2.company_id, Person.full_name, CPR2.relation_type)
                .join(alias_cpr1, alias_cpr1.person_id == CPR2.person_id)
                .join(Person, Person.id == alias_cpr1.person_id)
                .filter(alias_cpr1.company_id == current_id)
                .filter(CPR2.company_id != current_id)
                .limit(remaining_nodes * 2) # Fetch extra candidates
                .all()
            )

            for other_cid, person_name, rel_type in shared_person_results:
                if G.number_of_nodes() >= limit and str(other_cid) not in G.nodes:
                    break
                
                # Add Edge
                # We don't have the other company's name yet if it's new.
                # BFS Logic: Add to queue if new.
                other_node_id = str(other_cid)
                
                if other_node_id not in visited_companies:
                    # To display the label immediately (before visiting), we must fetch it?
                    # Or BFS structure implies we add edge now, but Node details populated when we Pop it?
                    # BUT: ForceGraph needs node to exist. 
                    # If we don't fetch/add node now, graph will have unknown target.
                    # So we MUST fetch the company details here or do a bulk fetch.
                    # Helper query to get unvan:
                    other_comp = self.db.query(Company).filter(Company.id == other_cid).first()
                    if other_comp:
                        # Add node immediately to graph (so edge is valid)
                        if other_node_id not in G.nodes:
                            if G.number_of_nodes() >= limit: break
                            G.add_node(other_node_id, label=other_comp.unvan, type="company",
                                       risk_status=self._check_risk_status(other_comp))
                            
                            if other_comp.koordinat is None:
                                missing_coords.add(str(other_comp.id))
                            
                            # Extract Features for new node
                            if other_node_id not in node_features_map:
                                node_features_map[other_node_id] = self._get_node_features(other_comp)

                            queue.append((other_cid, current_depth + 1))
                        
                        # Add Edge
                        # Label: "Ortak: AHM** YIL***"
                        # Apply masking
                        safe_name = self._mask_name(person_name)
                        edge_label = f"Ortak: {safe_name}"
                        G.add_edge(str(current_id), other_node_id, 
                                   label=edge_label, type="shared_person")

            # 4. Find Neighbors via Shared Address
            if comp.address:
                # Direct string match on address (fast)
                same_addr_results = (
                    self.db.query(Company)
                    .filter(Company.address == comp.address)
                    .filter(Company.id != current_id)
                    .limit(remaining_nodes)
                    .all()
                )
                
                for other_comp in same_addr_results:
                     other_node_id = str(other_comp.id)
                     if G.number_of_nodes() >= limit and other_node_id not in G.nodes:
                         break
                     
                     if other_node_id not in G.nodes:
                        G.add_node(other_node_id, label=other_comp.unvan, type="company",
                                   risk_status=self._check_risk_status(other_comp))
                        
                        if other_comp.koordinat is None:
                            missing_coords.add(str(other_comp.id))
                        
                        # Extract Features for new node
                        if other_node_id not in node_features_map:
                            node_features_map[other_node_id] = self._get_node_features(other_comp)

                        queue.append((other_comp.id, current_depth + 1))
                     
                     G.add_edge(str(current_id), other_node_id, 
                                label="Aynı Adres", type="same_address")


        # --- Analysis Phase ---
        
        # 1. Cycle Detection
        try:
            cycles = list(nx.simple_cycles(G))
        except Exception:
            cycles = []

        # 2. AI Anomaly Detection
        # (Feature map already contains intrinsic global_degree)
        
        # Run ML Model
        detector = NexusAnomalyDetector()
        anomaly_scores = detector.detect_anomalies(list(node_features_map.values()))
        
        # Update Node Status based on AI
        for nid, score in anomaly_scores.items():
            if nid in G.nodes:
                G.nodes[nid]['anomaly_score'] = score
                # Interpret Score: Lower is more anomalous. 
                # -1.0 to -0.1 is usually considered anomalous in robust datasets.
                # In small local graphs, -0.05 is a safe bet for "Standing out".
                if score < -0.05:
                    current_risk = G.nodes[nid].get('risk_status')
                    if current_risk != 'HIGH':
                        G.nodes[nid]['risk_status'] = 'HIGH'
                        G.nodes[nid]['risk_reason'] = f'AI Detected Anomaly (Score: {score:.2f})'

        # 3. Address Risk (Visualization)
        suspicious_addresses = [addr for addr, comps in address_map.items() if len(comps) > 3]

        # 4. Contagion Risk
        risky_neighbors = []
        for node, attrs in G.nodes(data=True):
            if attrs.get('risk_status') == 'HIGH':
                if node != str(target_company_id):
                    risky_neighbors.append(attrs.get('label'))

        # Construct Response
        response_graph = {
            "nodes": [{"id": n, **attr} for n, attr in G.nodes(data=True)],
            "links": [{"source": u, "target": v, **attr} for u, v, attr in G.edges(data=True)]
        }
        
        return {
            "graph": response_graph,
            "analysis": {
                "cycle_detected": len(cycles) > 0,
                "cycles_count": len(cycles),
                "suspicious_addresses": suspicious_addresses,
                "risky_neighbors": risky_neighbors,
                "total_nodes": G.number_of_nodes(),
                "total_edges": G.number_of_edges(),
                "limit_reached": G.number_of_nodes() >= limit,
                "ai_enabled": True,
                "missing_coords": list(missing_coords)
            }
        }

    def _check_risk_status(self, company: Company) -> str:
        """
        Determines risk level based on keywords in company name or announcements.
        Real implementation would look at 'Announcement' types for 'KONKORDATO', 'İFLAS'.
        """
        # 1. Check Announcements
        # This is simplified. In prod, we'd query the Announcements table joined.
        # For now, let's assume if the company name contains 'TASFİYE' it's risky.
        if company.unvan and "TASFİYE" in company.unvan:
             return "HIGH"
        
        # 2. Check Announcements (Query db)
        # Note: This checks specific keywords in the announcement history
        has_bad_news = self.db.query(Announcement).filter(
            Announcement.company_id == company.id,
            or_(
                Announcement.title.ilike("%İFLAS%"),
                Announcement.title.ilike("%KONKORDATO%"),
                Announcement.announcement_type.ilike("%İFLAS%"),
                Announcement.announcement_type.ilike("%KONKORDATO%")
            )
        ).first()

        if has_bad_news:
             return "HIGH"

        return "LOW"
