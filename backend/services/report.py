
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os, datetime

def generate_weekly_pdf(farm_id: str, data: dict, output_path: str):
    c = canvas.Canvas(output_path, pagesize=letter)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50,750, f"CropShield Weekly Report - {farm_id}")
    c.setFont("Helvetica", 10)
    c.drawString(50,730, f"Date: {datetime.date.today()} | IPFS Proof: {data.get('ipfs_cid','Qm...')[:20]}")
    c.drawString(50,710, f"NDVI: {data.get('ndvi',0):.2f} | NDMI: {data.get('ndmi',0):.2f} | Stress: {data.get('stress_pct',0):.1f}%")
    c.drawString(50,690, f"Weather: SPI {data.get('weather',{}).get('spi_proxy',0):.2f} | Heat days: {data.get('weather',{}).get('heat_days_7d',0)}")
    c.drawString(50,670, f"Payout: {data.get('payout_trigger',{}).get('payout_pct',0)}% - {data.get('payout_trigger',{}).get('reasons',[])}")
    c.drawString(50,650, f"Yield Est: {data.get('yield_estimate_bu_ac',0)} bu/ac")
    c.drawString(50,620, "Satellite image hash pinned to IPFS for auditability. Full data at https://ipfs.io/ipfs/"+data.get('ipfs_cid',''))
    c.save()
    return output_path

def send_report_email(farm_email: str, pdf_path: str):
    print(f"[EMAIL MOCK] Sending report to {farm_email} with {pdf_path}")
    # In prod: use SendGrid
    # import sendgrid; sg = SendGridAPIClient(os.getenv("SENDGRID_KEY"))
