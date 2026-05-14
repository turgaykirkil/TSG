import networkx as nx
from sqlalchemy.orm import Session, aliased
from sqlalchemy import or_, func, text
from app.models.company import Company
from app.models.person import Person
from app.models.relation import CompanyPersonRelation
from app.models.announcement import Announcement
from app.models.ocr_result import OcrResult
from app.nexus.ml.features import extract_capital, calculate_sector_entropy
from app.nexus.ml.anomaly import NexusAnomalyDetector, __name__ as anomaly_logger_name
from uuid import UUID
import logging

logger = logging.getLogger(__name__)

class NexusGraphService:
    def __init__(self, db: Session):
        self.db = db

    def _normalize_location(self, address: str) -> str:
        """
        Robust location normalization to detect shared addresses across different formats.
        Removes punctuation, standardizes common abbreviations.
        """
        if not address:
            return "UNKNOWN"
        import re
        # Standardize abbreviations and case
        s = address.upper()
        s = s.replace("MAHALLESİ", "MAH").replace("SOKAĞI", "SK").replace("SOKAK", "SK").replace("CADDESİ", "CAD")
        s = s.replace("SİTESİ", "SIT").replace("BLOK", "BLK").replace("NUMARA", "NO")
        
        # Remove punctuation
        s = re.sub(r'[^A-Z0-9\s]', ' ', s)
        # Squash spaces
        cleaned = " ".join(s.split())
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
        
    def _populate_graph_metadata(self, G):
        """
        Populates metadata (labels, risk statuses, addresses) for all nodes in the graph in BULK.
        Crucial for performance when limit > 20 over a slow SSH tunnel.
        """
        node_ids = [n for n in G.nodes]
        if not node_ids: return

        # Bulk fetch companies
        companies = {str(c.id): c for c in self.db.query(Company).filter(Company.id.in_(node_ids)).all()}
        
        # Determine risk status for each in bulk if possible
        # For now, we'll iterate the fetched objects once (fast as they are in-memory)
        for nid in node_ids:
            comp = companies.get(nid)
            if comp:
                G.nodes[nid].update({
                    "label": comp.unvan,
                    "address": comp.address,
                    "risk_status": self._check_risk_status(comp)
                })

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

            # 1. Fetch Company details if not fetched
            if current_id not in visited_companies:
                comp = self.db.query(Company).filter(Company.id == current_id).first()
                if not comp:
                    continue
            else:
                # Need to use existing node or fetch if not in context
                # Generally current_id should be in visited if we reached here
                pass # Already processed its neighbors

            visited_companies.add(current_id)

            # 2. Add Node
            # Colors/Types: "company" is standard. "target" can be distinguished by ID in UI.
            G.add_node(str(comp.id), label=comp.unvan, type="company", 
                       risk_status="LOW") # Default status, will be populated at end

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
                norm_addr = self._normalize_location(comp.address)
                # Direkt sorgula (N+1 değil, sadece 1 kez hedef için)
                total_at_address = self.db.query(Company).filter(
                    Company.address == comp.address,
                    Company.id != comp.id
                ).count()

                if total_at_address > 3:
                     # Mark this address as suspicious in the map conceptually
                     # We'll use a special key for global risks
                     address_map[f"GLOBAL_RISK::{norm_addr}"] = ["DUMMY"] * total_at_address

            remaining_nodes = limit - G.number_of_nodes()
            if remaining_nodes <= 0:
                break

            # 3. Find Neighbors via Shared Persons
            from sqlalchemy.orm import aliased
            CPR2 = aliased(CompanyPersonRelation)
            alias_cpr1 = CompanyPersonRelation

            shared_person_results = (
                self.db.query(CPR2.company_id, Person.full_name, CPR2.relation_type)
                .join(alias_cpr1, alias_cpr1.person_id == CPR2.person_id)
                .join(Person, Person.id == alias_cpr1.person_id)
                .filter(alias_cpr1.company_id == current_id)
                .filter(CPR2.company_id != current_id)
                .limit(remaining_nodes * 2)
                .all()
            )

            # BULK FETCH: tüm yeni komşu şirketleri tek sorguda al (N+1'i önler)
            new_cids = [
                other_cid for other_cid, _, _ in shared_person_results
                if str(other_cid) not in visited_companies and str(other_cid) not in G.nodes
            ]
            if new_cids:
                bulk_companies = {
                    str(c.id): c for c in
                    self.db.query(Company).filter(Company.id.in_(new_cids)).all()
                }
            else:
                bulk_companies = {}

            for other_cid, person_name, rel_type in shared_person_results:
                if G.number_of_nodes() >= limit and str(other_cid) not in G.nodes:
                    break

                other_node_id = str(other_cid)

                if other_node_id not in visited_companies:
                    other_comp = bulk_companies.get(other_node_id)
                    if other_comp:
                        if other_node_id not in G.nodes:
                            if G.number_of_nodes() >= limit: break
                            G.add_node(other_node_id, label=other_comp.unvan, type="company",
                                       risk_status="LOW") # Optimized: No per-node risk check here

                            if other_comp.koordinat is None:
                                missing_coords.add(str(other_comp.id))

                            queue.append((other_cid, current_depth + 1))
                        
                        # Add Edge
                        # Label: "Ortak: AHM** YIL***"
                        # Apply masking
                        safe_name = self._mask_name(person_name)
                        edge_label = f"Ortak: {safe_name}"
                        G.add_edge(str(current_id), other_node_id, 
                                   label=edge_label, type="shared_person")

            # 4. Find Neighbors via Exact String Address Match (Moved out of loop)
            if comp.address:
                remaining_nodes = limit - G.number_of_nodes()
                if remaining_nodes > 0:
                    # Strategy: Find a unique part of the address (e.g. building name) 
                    # and search with ILIKE %part% to catch variations like 'Mah.' vs 'Mahallesi'
                    addr_parts = comp.address.strip().upper().split()
                    unique_prefix = " ".join(addr_parts[2:6]) if len(addr_parts) > 5 else " ".join(addr_parts[:4])

                    same_addr_query = text("""
                        SELECT id, unvan FROM app.companies 
                        WHERE id != :current_id 
                          AND tr_normalize(address) ILIKE '%' || tr_normalize(:prefix) || '%'
                        LIMIT :limit
                    """)
                    same_addr_results = self.db.execute(same_addr_query, {
                        "current_id": current_id, 
                        "prefix": unique_prefix,
                        "limit": remaining_nodes
                    }).fetchall()
                    
                    for other_cid, other_unvan in same_addr_results:
                        if G.number_of_nodes() >= limit and str(other_cid) not in G.nodes:
                            break
                        
                        other_node_id = str(other_cid)
                        if other_node_id not in visited_companies:
                            queue.append((other_cid, current_depth + 1))
                            if other_node_id not in G.nodes:
                                G.add_node(other_node_id, label=other_unvan, type="company", risk_status='UNKNOWN')
                                       
                        # Prevent duplicate edges
                        if not G.has_edge(str(current_id), other_node_id):
                            G.add_edge(str(current_id), other_node_id, label="Aynı Adres", type="shared_address")

            # 5. Deep Discovery: Removed obsolete ocr_person_mentions block.
            # Person relations are already handled above in "3. Find Neighbors via Shared Persons"

            # 6. Find Neighbors via PostGIS Geographic Radius (50 meters)
            if comp.koordinat is not None:
                # ST_DWithin distance parameter is in meters if geography is used. 
                # If geometry with SRID 4326 is used, distance is in degrees (bad for accuracy).
                # We cast to geography to specify meters safely: ST_DWithin(koordinat::geography, target::geography, 50)
                
                # Fetch up to limit remaining neighbors within 50 meters
                geo_query = text("""
                    SELECT id, unvan, ST_AsText(koordinat) 
                    FROM app.companies 
                    WHERE id != :current_id 
                      AND koordinat IS NOT NULL
                      AND ST_DWithin(koordinat::geography, :current_coord::geography, 50)
                    LIMIT :limit
                """)
                # extract WKT string for the parameter
                # We need to get the WKT value of comp.koordinat
                # since comp.koordinat is a WKBElement or string depending on loading,
                # the safest way without another query is if we already fetched it as text,
                # but we can also use SQL purely by nesting the point.
                
                # PRE-OPTIMIZATION: Fetch target coord first to avoid scalar subquery overhead
                target_coord = self.db.execute(text("SELECT ST_AsText(koordinat) FROM app.companies WHERE id = :id"), {"id": current_id}).scalar()
                
                if target_coord:
                    nested_geo_query = text("""
                        SELECT id, unvan 
                        FROM app.companies
                        WHERE id != :current_id 
                          AND koordinat IS NOT NULL
                          AND ST_DWithin(koordinat::geography, ST_GeogFromText(:target_coord), 50)
                        LIMIT :limit
                    """)
                    
                    same_geo_results = self.db.execute(nested_geo_query, {
                        "current_id": current_id, 
                        "target_coord": target_coord,
                        "limit": remaining_nodes
                    }).fetchall()
                
                for other_cid, other_unvan in same_geo_results:
                     other_node_id = str(other_cid)
                     if G.number_of_nodes() >= limit and other_node_id not in G.nodes:
                         break
                     
                     if other_node_id not in G.nodes:
                        # Full fetch for features (we could optimize this further but it's a start)
                        other_comp = self.db.query(Company).filter(Company.id == other_cid).first()
                        if other_comp:
                            G.add_node(other_node_id, label=other_unvan, type="company",
                                       risk_status=self._check_risk_status(other_comp))
                            
                            # Extract Features for new node
                            if other_node_id not in node_features_map:
                                node_features_map[other_node_id] = self._get_node_features(other_comp)

                            queue.append((other_comp.id, current_depth + 1))
                     
                     G.add_edge(str(current_id), other_node_id, 
                                label="Fizyolojik Yakınlık (50m)", type="same_address")
            elif comp.address:
                # Fallback to string matching if coordinates are missing
                missing_coords.add(str(comp.id))
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

            # 6. Cross-company Person mentions: Removed obsolete ocr_person_mentions block


        # --- Analysis Phase ---
        
        # 1. Cycle Detection
        try:
            cycles = list(nx.simple_cycles(G))
        except Exception:
            cycles = []

        # 2. AI Anomaly Detection
        # (Feature map already contains intrinsic global_degree)
        
        # Run ML Model Later in Background
        # We prepare the features and just return the structured data immediately.
        # Background tasks will update the nodes in DB or Cache.
        # For now, UI will just show neutral risk unless pre-calculated or set by quick heuristics.
        

        # --- [BULK POPULATE NODES] ---
        # Instead of querying for every node in the loop, we do it ONCE here
        self._populate_graph_metadata(G)

        # 3. Address Risk (Visualization)
        suspicious_addresses = [addr for addr, comps in address_map.items() if len(comps) > 3]

        # 4. Contagion Risk
        risky_neighbors = []
        for node, attrs in G.nodes(data=True):
            if attrs.get('risk_status') == 'HIGH':
                if node != str(target_company_id):
                    risky_neighbors.append(attrs.get('label'))

        # 5. Network-Based Fraud Scoring
        target_comp = self.db.query(Company).filter(Company.id == target_company_id).first()
        target_address = target_comp.address if target_comp else None
        fraud_score, fraud_signals, fraud_meta = self._score_network_fraud(
            G=G,
            target_company_id=str(target_company_id),
            address_map=address_map,
            target_address=target_address
        )

        # Construct Response
        response_graph = {
            "nodes": [{"id": n, **attr} for n, attr in G.nodes(data=True)],
            "links": [{"source": u, "target": v, **attr} for u, v, attr in G.edges(data=True)]
        }
        
        return {
            "graph": response_graph,
            "analysis": {
                "cycle_detected": len(cycles) > 0 or fraud_meta.get('cycle_detected', False),
                "cycles_count": max(len(cycles), 1 if fraud_meta.get('cycle_detected') else 0),
                "suspicious_addresses": suspicious_addresses if not target_address else [target_address] if fraud_meta.get('total_at_addr', 0) > 3 else [],
                "risky_neighbors": risky_neighbors or ([f"DB:{fraud_meta.get('risky_at_addr')} Riskli"] if fraud_meta.get('risky_at_addr', 0) > 0 else []),
                "fraud_score": fraud_score,
                "fraud_signals": fraud_signals,
                "fraud_meta": fraud_meta,
                "fraud_level": "HIGH" if fraud_score >= 5 else "MEDIUM" if fraud_score >= 2 else "LOW",
                "total_nodes": G.number_of_nodes(),
                "total_edges": G.number_of_edges(),
                "limit_reached": G.number_of_nodes() >= limit,
                "ai_enabled": True,
                "missing_coords": list(missing_coords),
                "ml_features_payload": list(node_features_map.values()) # Passed to bg task
            }
        }
        
    def run_background_anomaly_detection(self, features_payload: list):
        """
        Background Task: Runs the heavy Unsupervised Learning pipeline and updates the cache/DB.
        """
        if not features_payload:
            return
            
        try:
            logger.info(f"Running Background ML Anomaly Detection on {len(features_payload)} nodes.")
            detector = NexusAnomalyDetector()
            anomaly_scores = detector.detect_anomalies(features_payload)
            
            # FUTURE: Save these scores to a database table or Redis cache so they 
            # are instantly available on the next user request.
            # For now, we just execute it to ensure the pipeline runs without blocking the API.
            
        except Exception as e:
            logger.error(f"Background ML Anomaly Detection failed: {e}")

    def _check_risk_status(self, company: Company) -> str:
        """
        Node-level risk: bankruptcy/liquidation signals from announcements.
        Network-level fraud is handled separately by _score_network_fraud.
        """
        if company.unvan and any(kw in company.unvan for kw in ["TASFİYE", "KONKORDATO", "İFLAS"]):
            return "HIGH"

        has_bad_news = self.db.query(Announcement).filter(
            Announcement.company_id == company.id,
            or_(
                Announcement.title.ilike("%İFLAS%"),
                Announcement.title.ilike("%KONKORDATO%"),
                Announcement.title.ilike("%HACİZ%"),
                Announcement.announcement_type.ilike("%İFLAS%"),
                Announcement.announcement_type.ilike("%KONKORDATO%")
            )
        ).first()

        if has_bad_news:
            return "HIGH"

        return "LOW"

    def _score_network_fraud(self, G, target_company_id: str, address_map: dict, target_address: str = None) -> tuple:
        """
        Network tabanlı fraud skor motoru.
        Graf kenarlarının KOMBİNASYONUNA bakar — tek şirkete değil.

        Fraud yolları:
          +3 → Aynı (kişi + adres) çakışması: shared_person + shared_address aynı çift
          +2 → Seri ortak: Bir kişi grafın 5+ farklı şirketinde ortak
          +2 → Adres yoğunlaşması: Aynı normalleştirilmiş adreste 4+ şirket
          +3 → Contagion: Komşu düğüm risk_status=HIGH (iflasçı ortak)
          +1 → Döngü: Ortak/adres döngüsü (circular ownership şüphesi)

        Returns: (fraud_score: int, fraud_signals: list[str])
        """
        score = 0
        signals = []
        meta = {"total_at_addr": 0, "risky_at_addr": 0, "cycle_detected": False}

        # --- [1] Aynı kişi + aynı adres çakışması ---
        # Bir çift düğüm arasında hem shared_person hem shared_address kenarı varsa → kırmızı bayrak
        person_edges = set()  # (u, v) çiftleri
        address_edges = set()

        for u, v, data in G.edges(data=True):
            pair = tuple(sorted([u, v]))
            if data.get('type') == 'shared_person':
                person_edges.add(pair)
            elif data.get('type') in ('shared_address', 'same_address'):
                address_edges.add(pair)

        overlapping_pairs = person_edges & address_edges
        if overlapping_pairs:
            score += 3 * len(overlapping_pairs)
            signals.append(
                f"{len(overlapping_pairs)} çift şirket hem ortak hem adres paylaşıyor "
                f"(klasik fraud yapısı)"
            )

        # --- [2] Seri ortak tespiti ---
        # Bir kişi adı grafın 5+ kenarında geçiyorsa → seri ortak
        person_edge_count: dict = {}
        for u, v, data in G.edges(data=True):
            if data.get('type') == 'shared_person':
                label = data.get('label', '')
                person_edge_count[label] = person_edge_count.get(label, 0) + 1

        serial_persons = [p for p, cnt in person_edge_count.items() if cnt >= 5]
        if serial_persons:
            score += 2 * len(serial_persons)
            signals.append(
                f"{len(serial_persons)} kişi 5+ farklı şirkette ortak "
                f"(seri ortak riski): {', '.join(serial_persons[:3])}"
            )

        # --- [3] Adres yoğunlaşması — DB'den doğrudan sorgula (in-memory map güvenilmez) ---
        if target_address:
            try:
                # Aynı adreste kaç şirket var (tr_normalize ile)
                addr_parts = target_address.strip().upper().split()
                search_prefix = " ".join(addr_parts[2:6]) if len(addr_parts) > 5 else " ".join(addr_parts[:4])

                addr_count_q = text("""
                    SELECT COUNT(*) FROM app.companies
                    WHERE id != :cid
                      AND tr_normalize(address) ILIKE '%' || tr_normalize(:pfx) || '%'
                """)
                total_at_addr = self.db.execute(addr_count_q, {
                    "cid": target_company_id, "pfx": search_prefix
                }).scalar() or 0

                # Aynı adreste TASFİYE/İFLAS firma sayısı
                risky_at_addr_q = text("""
                    SELECT COUNT(*) FROM app.companies
                    WHERE id != :cid
                      AND tr_normalize(address) ILIKE '%' || tr_normalize(:pfx) || '%'
                      AND (unvan ILIKE '%tasfiye%' OR unvan ILIKE '%iflas%' OR unvan ILIKE '%konkordato%')
                """)
                risky_at_addr = self.db.execute(risky_at_addr_q, {
                    "cid": target_company_id, "pfx": search_prefix
                }).scalar() or 0

                if total_at_addr >= 10:
                    score += 3
                    signals.append(
                        f"Aynı adreste {total_at_addr} firma var — çok yoğun paravan adres riski"
                    )
                elif total_at_addr >= 4:
                    score += 2
                    signals.append(
                        f"Aynı adreste {total_at_addr} firma var (adres yoğunlaşması)"
                    )

                if risky_at_addr >= 5:
                    score += 3
                    signals.append(
                        f"Aynı adreste {risky_at_addr} TASFİYE/İFLAS firması var — yüksek contagion riski"
                    )
                elif risky_at_addr >= 2:
                    score += 2
                    signals.append(
                        f"Aynı adreste {risky_at_addr} TASFİYE/İFLAS firması var"
                    )
                
                meta["total_at_addr"] = total_at_addr
                meta["risky_at_addr"] = risky_at_addr

            except Exception as e:
                logger.warning(f"Adres yoğunluk sorgusu başarısız: {e}")
        else:
            # Fallback: in-memory map
            dense_addresses = [
                addr for addr, comps in address_map.items()
                if not addr.startswith('GLOBAL_RISK::') and len(comps) >= 4
            ]
            if dense_addresses:
                score += 2
                signals.append(
                    f"{len(dense_addresses)} adreste 4+ şirket yoğunlaşması (adres bombası şüphesi)"
                )
                meta["total_at_addr"] = len(dense_addresses[0]) # approx

        # --- [4] Contagion: Komşu iflasçı/riskli şirket ---
        target_neighbors = list(G.neighbors(target_company_id)) if target_company_id in G else []
        high_risk_neighbors = [
            G.nodes[n].get('label', n)
            for n in target_neighbors
            if G.nodes[n].get('risk_status') == 'HIGH'
        ]
        if high_risk_neighbors:
            score += 3
            signals.append(
                f"Doğrudan bağlı {len(high_risk_neighbors)} riskli komşu: "
                f"{', '.join(high_risk_neighbors[:3])}"
            )

        # --- [5] Döngü tespiti (Pahalıdır, büyük graflarda limitle) ---
        if G.number_of_nodes() < 50:
            try:
                import networkx as nx
                cycles = list(nx.simple_cycles(G))
                if cycles:
                    score += 1
                    signals.append(f"{len(cycles)} döngüsel bağlantı tespit edildi")
                    meta["cycle_detected"] = True
            except Exception as e:
                logger.debug(f"Cycle detection skipped: {e}")
        else:
            # Sadece hedef düğümün dahil olduğu basit bir kontrol denenebilir
            # Ama performans için şimdilik tamamen atlayalım
            pass

        return score, signals, meta
