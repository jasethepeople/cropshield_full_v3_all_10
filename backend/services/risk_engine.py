
def evaluate_triggers(weather, indices):
    payout_pct = 0
    reasons = []
    if weather["drought_trigger_met"] or indices["ndmi_mean"] < 0.1:
        payout_pct = max(payout_pct, 40)
        reasons.append(f"Drought SPI {weather['spi_proxy']:.2f}")
    if weather["heat_trigger_met"]:
        payout_pct = max(payout_pct, 60)
        reasons.append(f"Heat {weather['heat_days_7d']} days")
    if indices["stress_pct"] > 35:
        payout_pct = max(payout_pct, 30)
        reasons.append(f"Stress {indices['stress_pct']:.1f}%")
    return {"payout_pct": payout_pct, "triggered": payout_pct>0, "reasons": reasons}

def get_oracle_payload(farm_id):
    return {"farm_id": farm_id, "spi": -1.8, "temp": 39.2, "payout_pct": 60, "ipfs_hash": "QmTestHash123"}
