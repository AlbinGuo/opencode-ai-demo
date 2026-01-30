import os

GITEE_CLIENT_ID = os.getenv("GITEE_CLIENT_ID", "")
GITEE_CLIENT_SECRET = os.getenv("GITEE_CLIENT_SECRET", "")
GITEE_REDIRECT_URI = os.getenv("GITEE_REDIRECT_URI", "http://localhost:3006/auth/gitee/callback")

GITEE_AUTH_URL = "https://gitee.com/oauth/authorize"
GITEE_TOKEN_URL = "https://gitee.com/oauth/token"
GITEE_USER_API = "https://gitee.com/api/v5/user"
