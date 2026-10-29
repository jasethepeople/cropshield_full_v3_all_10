
import os
from twilio.rest import Client

def send_payout_sms(phone: str, farm_name: str, amount: float, reason: str, tx_hash: str):
    sid = os.getenv("TWILIO_SID")
    token = os.getenv("TWILIO_TOKEN")
    from_num = os.getenv("TWILIO_FROM")
    if not sid:
        print(f"[SMS MOCK] To {phone}: {farm_name} payout ${amount} - {reason} tx:{tx_hash}")
        return {"mock": True}
    client = Client(sid, token)
    msg = f"CropShield: {farm_name}, payout ${amount:.2f} triggered. Reason: {reason}. Tx: {tx_hash[:10]}... USDC sent. No action needed."
    m = client.messages.create(body=msg, from_=from_num, to=phone)
    return {"sid": m.sid}

def send_stress_alert(phone: str, farm_name: str, stress_pct: float, sector: str="B4"):
    sid = os.getenv("TWILIO_SID")
    if not sid:
        print(f"[SMS MOCK] Alert {phone}: {stress_pct}% stress in {sector}")
        return
    client = Client(os.getenv("TWILIO_SID"), os.getenv("TWILIO_TOKEN"))
    client.messages.create(body=f"CropShield Alert: {farm_name} sector {sector} showing {stress_pct:.0f}% stress. Check app.", from_=os.getenv("TWILIO_FROM"), to=phone)
