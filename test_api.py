import requests

seq = "MKTAYIAKQRQISFVKSHFSRQ"
url = "https://api.esmatlas.com/foldSequence/v1/pdb/"

r = requests.post(url, data=seq, timeout=60)
print("Status:", r.status_code)
print(r.text[:400])