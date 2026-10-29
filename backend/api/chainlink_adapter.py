
from fastapi import APIRouter
router = APIRouter()

@router.post("/chainlink/execute")
def chainlink_execute(payload: dict):
    # Chainlink Functions calls this
    farm_id = payload.get("farm_id")
    # Run full analysis
    from services import satellite, weather, risk_engine, ipfs
    # ... load polygon from DB by farm_id
    # mocked for turnkey
    result = {"spi": -18, "temp": 3920, "payoutPct": 60, "ipfs": "QmHash", "reason": "Drought+Heat"}
    return result
