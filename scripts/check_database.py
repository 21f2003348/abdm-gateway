"""
Script to directly check database contents
Run this to see what's stored in the database
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.database import SessionLocal
from app.db.models import (
    Client, Bridge, BridgeService, LinkToken, 
    LinkTransaction, Consent, HealthData, DataRequest
)
from datetime import datetime

def print_table_data(table_name, data):
    print(f"\n{'='*60}")
    print(f"  {table_name} ({len(data)} records)")
    print(f"{'='*60}")
    if data:
        for item in data:
            print(f"  {item}")
    else:
        print("  (No records)")

def check_database():
    db = SessionLocal()
    try:
        print("\n" + "="*60)
        print("  DATABASE CONTENTS CHECK")
        print("="*60)
        
        # Check Clients
        clients = db.query(Client).all()
        print_table_data("CLIENTS", [
            f"ID: {c.client_id}, CM_ID: {c.cm_id}, Active: {c.is_active}"
            for c in clients
        ])
        
        # Check Bridges
        bridges = db.query(Bridge).all()
        print_table_data("BRIDGES", [
            f"ID: {b.bridge_id}, Type: {b.entity_type}, Name: {b.name}, Webhook: {b.webhook_url}"
            for b in bridges
        ])
        
        # Check Bridge Services
        services = db.query(BridgeService).all()
        print_table_data("BRIDGE SERVICES", [
            f"ID: {s.service_id}, Bridge: {s.bridge_id}, Name: {s.name}, Active: {s.active}"
            for s in services
        ])
        
        # Check Link Tokens
        tokens = db.query(LinkToken).all()
        print_table_data("LINK TOKENS", [
            f"Token: {t.token[:20]}..., Patient: {t.patient_id}, HIP: {t.hip_id}, Expires: {t.expires_at}"
            for t in tokens
        ])
        
        # Check Link Transactions
        txns = db.query(LinkTransaction).all()
        print_table_data("LINK TRANSACTIONS", [
            f"TXN_ID: {t.txn_id}, Patient: {t.patient_id}, Status: {t.status}, Created: {t.created_at}"
            for t in txns
        ])
        
        # Check Consents
        consents = db.query(Consent).all()
        print_table_data("CONSENTS", [
            f"ID: {c.consent_request_id}, Patient: {c.patient_id}, Status: {c.status}, Created: {c.created_at}"
            for c in consents
        ])
        
        # Check Health Data
        health_data = db.query(HealthData).all()
        print_table_data("HEALTH DATA", [
            f"TXN_ID: {h.txn_id}, Patient: {h.patient_id}, Status: {h.status}, Sent: {h.sent_at}"
            for h in health_data
        ])
        
        # Check Data Requests
        requests = db.query(DataRequest).all()
        print_table_data("DATA REQUESTS", [
            f"Request_ID: {r.request_id}, Patient: {r.patient_id}, Status: {r.status}, Created: {r.requested_at}"
            for r in requests
        ])
        
        print(f"\n{'='*60}")
        print("  SUMMARY")
        print(f"{'='*60}")
        print(f"  Clients: {len(clients)}")
        print(f"  Bridges: {len(bridges)}")
        print(f"  Services: {len(services)}")
        print(f"  Link Tokens: {len(tokens)}")
        print(f"  Transactions: {len(txns)}")
        print(f"  Consents: {len(consents)}")
        print(f"  Health Data: {len(health_data)}")
        print(f"  Data Requests: {len(requests)}")
        print(f"{'='*60}\n")
        
    except Exception as e:
        print(f"Error checking database: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    check_database()

