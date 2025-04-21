import os
import msal
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("APPLICATION_CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET_VALUE")
TENANT_ID = os.getenv("DIRECTORY_TENANT_ID")
SCOPES_STR = os.getenv("SCOPES")

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPE = SCOPES_STR.split() if SCOPES_STR else ["https://graph.microsoft.com/.default"]


def get_access_token():
    app = msal.ConfidentialClientApplication(
        CLIENT_ID, authority=AUTHORITY,
        client_credential=CLIENT_SECRET
    )
    result = app.acquire_token_for_client(scopes=SCOPE)

    if "access_token" in result:
        return result["access_token"]
    else:
        raise RuntimeError(f"Failed to acquire token: {result}")