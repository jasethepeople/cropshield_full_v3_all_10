
"""
Risk Marketplace - co-ops trade risk
Willard Co-op can sell 20% of its drought risk to Cache Valley Co-op
"""
from typing import List

class RiskMarketplace:
    def __init__(self):
        self.listings = [] # in-memory, use DB in prod
    
    def list_risk(self, coop_id: str, risk_type: str, amount: float, premium: float):
        listing = {"id": len(self.listings), "coop_id": coop_id, "risk_type": risk_type, "amount": amount, "premium": premium, "buyer": None}
        self.listings.append(listing)
        return listing
    
    def buy_risk(self, listing_id: int, buyer_coop: str):
        l = self.listings[listing_id]
        l["buyer"] = buyer_coop
        print(f"[MARKET] {buyer_coop} bought {l['risk_type']} risk ${l['amount']} from {l['coop_id']} for ${l['premium']}")
        return l
    
    def get_orderbook(self):
        return self.listings

marketplace = RiskMarketplace()
# Seed
marketplace.list_risk("willard_valley", "drought", 15000, 900)
marketplace.list_risk("cache_valley", "heat", 10000, 700)
