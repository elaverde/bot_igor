import dropbox
from dropbox import DropboxOAuth2FlowNoRedirect

APP_KEY = "q9jttaqe6trzi7c"
APP_SECRET = "6eyc980unt44pvy"

auth_flow = DropboxOAuth2FlowNoRedirect(
    APP_KEY,
    APP_SECRET,
    token_access_type="offline"
)

authorize_url = auth_flow.start()
print("1. Ve a este URL:")
print(authorize_url)
print()
code = input("2. Pega el código de autorización aquí: ").strip()

oauth_result = auth_flow.finish(code)
print()
print("✅ REFRESH TOKEN (guárdalo en .env):")
print(oauth_result.refresh_token)
