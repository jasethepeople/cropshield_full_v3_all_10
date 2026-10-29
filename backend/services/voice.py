
"""
Twilio Voice - farmer calls number, gets field status
"""
from fastapi import APIRouter
from fastapi.responses import Response

router = APIRouter()

@router.post("/voice/status")
def voice_status():
    # TwiML
    twiml = """<?xml version="1.0" encoding="UTF-8"?>
    <Response>
        <Say voice="Polly.Joanna">CropShield report for Clark Family Farm. NDVI is 68 percent, healthy. 21 day rain is 32 millimeters. No payout triggered. Your co-op pool is 78 thousand dollars. Goodbye.</Say>
    </Response>
    """
    return Response(content=twiml, media_type="application/xml")

@router.post("/voice/inbound")
def inbound_call():
    # In prod, lookup caller ID -> farm_id -> generate dynamic report
    return voice_status()
