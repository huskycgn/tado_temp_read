import requests

req = requests.post(
    "https://login.tado.com/oauth2/device_authorize",
    params=dict(
        client_id="1bb50063-6b0c-4d11-bd99-387f4a91cc46",
        scope="offline_access",
    ),
)

print(req.json())

device_id = input("Enter Device_ID: ")

req2 = requests.post(
    "https://login.tado.com/oauth2/token",
    params=dict(
        client_id="1bb50063-6b0c-4d11-bd99-387f4a91cc46",
        device_code=device_id,
        grant_type="urn:ietf:params:oauth:grant-type:device_code",
    ),
)

print(req2.json())

refresh_token = req2.json()["refresh_token"]
access_token = req2.json()["access_token"]

with open("refresh_token.txt", "w") as f:
    f.write(refresh_token)

with open("token.txt", "w") as f:
    f.write(access_token)
