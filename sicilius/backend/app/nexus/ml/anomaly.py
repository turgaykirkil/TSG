from sklearn.ensemble import IsolationForest
import numpy as np
from typing import List, Dict

class NexusAnomalyDetector:
    def __init__(self, contamination: float = 0.1):
        """
        :param contamination: Expected proportion of outliers (default 10%)
        """
        self.contamination = contamination
        self.model = IsolationForest(contamination=contamination, random_state=42)

    def detect_anomalies(self, nodes_data: List[Dict]) -> Dict[str, float]:
        """
        Detects anomalies in the provided list of company nodes.
        Feature vector per node: [log(capital), density, global_degree, title_len]
        """
        if not nodes_data or len(nodes_data) < 5:
            # Not enough data for meaningful ML
            return {node['id']: 0.0 for node in nodes_data}
            
        # 1. Prepare Feature Matrix
        X = []
        ids = []
        
        for node in nodes_data:
            cap = node.get('capital', 0)
            log_cap = np.log1p(cap)
            
            density = node.get('address_density', 1)
            # Use Intrinsic Global Degree (DB count), NOT Graph Degree
            global_degree = node.get('global_degree', 0)
            title_len = node.get('title_len', 10)
            entropy = node.get('address_entropy', 0.0)
            
            # Features: [Capital, Density, Connections, NameComplexity, SectorChaos]
            X.append([log_cap, density, global_degree, title_len, entropy])
            ids.append(node['id'])
            
        X = np.array(X)
        
        # 2. Fit and Predict
        self.model.fit(X)
        scores = self.model.decision_function(X)
        
        # 3. Map Scores
        result = {}
        for i, uid in enumerate(ids):
            result[uid] = float(scores[i])
            
        return result
