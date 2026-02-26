import requests
from keycloak_variables import kc_url, kc_realm, kc_client_id, kc_secret

def get_new_token():
    """
    Request a new Keycloak access token using Client Credentials flow.
    """
    if not kc_client_id or not kc_secret or not kc_url or not kc_realm:
        raise Exception("Missing keycloak_client_id, keycloak_client_secret, keycloak_url, or keycloak_realm")

    token_url = f"{kc_url}/realms/{kc_realm}/protocol/openid-connect/token"
    
    try:
        response = requests.post(
            token_url,
            data={
                "grant_type": "client_credentials",
                "client_id": kc_client_id,
                "client_secret": kc_secret,
            },
            timeout=10
        )

        if response.status_code != 200:
            # print("Failed to obtain Keycloak token:", response.status_code, response.text)
            raise Exception(f"Failed to obtain Keycloak token: {response.status_code} - {response.text}")

        token_data = response.json()
        # print("Successfully obtained new Keycloak token", token_data["access_token"])
        return token_data["access_token"]

    except Exception as e:
        raise Exception(f"Error requesting new Keycloak token: {e}")
        
    
if __name__ == "__main__":   
    get_new_token()
    