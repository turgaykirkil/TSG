import sys
import os
from uuid import UUID

# Add backend to path
sys.path.append(os.getcwd())

from app.db.session import SessionLocal
from app.nexus.graph_service import NexusGraphService

def verify_ai():
    db = SessionLocal()
    # VOLİDUS TEKNOLOJİ
    target_id = UUID("c0041c75-0768-4279-8c1e-939bc61ecfbe")
    
    try:
        service = NexusGraphService(db)
        print(f"🧠 Running Nexus AI Analysis for {target_id}...")
        
        # Limit 20 to get enough nodes for ML
        result = service.analyze_company_network(target_id, limit=20)
        
        analysis = result['analysis']
        graph = result['graph']
        
        print(f"\n✅ Analysis Complete. AI Enabled: {analysis.get('ai_enabled')}")
        print(f"Nodes: {analysis['total_nodes']}, Edges: {analysis['total_edges']}")
        
        print("\n--- AI Risk Warnings ---")
        ai_risks = [n for n in graph['nodes'] if 'AI Detected Anomaly' in str(n.get('risk_reason', ''))]
        
        if ai_risks:
            for node in ai_risks:
                print(f"🔴 AI ALERT: {node['label']}")
                print(f"   Score: {node.get('anomaly_score')}")
                print(f"   Reason: {node.get('risk_reason')}")
        else:
            print("🟢 No AI Anomalies detected in this sample (Normal behavior for uniform data).")
            
        print("\n--- Node Features/scores (Top 5) ---")
        for node in graph['nodes'][:5]:
            score = node.get('anomaly_score', 'N/A')
            status = node.get('risk_status')
            print(f"   {node['label'][:30]}... -> Score: {score} ({status})")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    verify_ai()
