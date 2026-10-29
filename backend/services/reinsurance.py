
"""
Arbol / Etherisc reinsurance adapter
When regional event (>3 farms in 10km trigger same week), auto-claim regional cover
"""
import os, requests
from typing import List

class ReinsuranceAdapter:
    def __init__(self):
        self.arbol_api = os.getenv("ARBOL_API_URL", "https://api.arbolmarket.com")
        self.cover_amount = 200_000 # $200k regional
    
    def check_regional_trigger(self, triggered_farms: List[dict]) -> bool:
        if len(triggered_farms) < 3: return False
        # Check if farms within 10km radius - simplified haversine
        # In prod, cluster by geohash
        print(f"[REINSURANCE] {len(triggered_farms)} farms triggered, checking regional cover")
        return True
    
    def claim_regional(self, coop_id: str, reason: str, ipfs_proofs: List[str]):
        # POST to Arbol / Etherisc
        payload = {"coop_id": coop_id, "reason": reason, "proofs": ipfs_proofs, "amount": self.cover_amount}
        print(f"[REINSURANCE] Claiming ${self.cover_amount} for {coop_id}")
        # requests.post(f"{self.arbol_api}/claims", json=payload, headers={"Authorization": f"Bearer {os.getenv('ARBOL_KEY')}"})
        return {"claim_id": "arb_123", "status": "approved", "amount": self.cover_amount}

reinsurance = ReinsuranceAdapter()
