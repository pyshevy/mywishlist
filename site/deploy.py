from pprint import pprint
from urllib.parse import urljoin

import requests


api_token = "54aa702700b688e867f74125dfb55ba8a50a10bd"
headers = {"Authorization": f"Token {api_token}"}

username = "shevskii"  # update to match your USERNAME!

# or "eu.pythonanywhere.com" if your account is hosted on our EU servers
pythonanywhere_host = "www.pythonanywhere.com"
pythonanywhere_domain = "pythonanywhere.com"  # or "eu.pythonanywhere.com"

# make sure you don't use this domain already!
domain_name = f"{username}.{pythonanywhere_domain}"

api_base = f"https://{pythonanywhere_host}/api/v1/user/{username}/"
command = (
    f"/home/{username}/MyWishlist/venv/bin/uvicorn "
    "--uds $DOMAIN_SOCKET "
    "MyWishlist.sit.main:app "
)

response = requests.post(
    urljoin(api_base, "websites/"),
    headers=headers,
    json={
        "domain_name": domain_name,
        "enabled": True,
        "webapp": {"command": command}
    },
)
pprint(response.json())
