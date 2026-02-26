from decouple import config

try:
    kc_url = config("KC_URL")
    kc_realm = config("KC_REALM")
    kc_client_id = config("KC_CLIENT_ID")
    kc_secret = config("KC_SECRET")
except Exception as e:
    raise Exception(
        f"""Required environment variable '{e.__str__().split(' ')[0]}' not found.
 Reference the .env.example file of this project for required variables"""
    )