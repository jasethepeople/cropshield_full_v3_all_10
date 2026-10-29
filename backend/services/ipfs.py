
import os, requests
def pin_json(data):
    jwt = os.getenv("PINATA_JWT")
    if not jwt:
        return "QmMockCID_"+data.get("farm_id","test")
    url = "https://api.pinata.cloud/pinning/pinJSONToIPFS"
    headers = {"Authorization": f"Bearer {jwt}"}
    r = requests.post(url, json=data, headers=headers)
    return r.json().get("IpfsHash", "QmError")
