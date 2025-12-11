import networkx as nx
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.company import Company
from app.models.person import Person
from app.models.relation import CompanyPersonRelation
from app.models.announcement import Announcement
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

    def analyze_company_network(self, target_company_id: UUID, depth: int = 2, limit: int = 10) -> dict:
        """
        Builds a relationship graph of Companies ONLY.
        Companies are linked if they share a Person or an Address.
        """
        G = nx.DiGraph()
        
        visited_companies = set()
        queue = [(target_company_id, 0)]
        
        # Address map for risk analysis
        address_map = {}

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
                 # Count all companies with this exact address in DB
                 total_at_address = self.db.query(Company).filter(Company.address == comp.address).count()
                 if total_at_address > 3:
                     # Mark this address as suspicious in the map conceptually, even if nodes aren't in graph
                     # valid way: store in a separate set or just ensure analysis phase catches it.
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
                        queue.append((other_comp.id, current_depth + 1))
                     
                     G.add_edge(str(current_id), other_node_id, 
                                label="Aynı Adres", type="same_address")


        # --- Analysis Phase ---
        
        # 1. Cycle Detection
        try:
            cycles = list(nx.simple_cycles(G))
        except Exception:
            cycles = []

        # 2. Address Risk
        suspicious_addresses = [addr for addr, comps in address_map.items() if len(comps) > 3]

        # 3. Contagion Risk
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
                "limit_reached": G.number_of_nodes() >= limit
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
