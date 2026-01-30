import os

GITEE_CLIENT_ID = os.getenv("GITEE_CLIENT_ID", "48f86608a1b09bb3fb5dff0ab480458e258647d4230a2090362720a6bb3035cf")
GITEE_CLIENT_SECRET = os.getenv("GITEE_CLIENT_SECRET", "87ca939fa48bd388eb88527bd5e3f2b3f22d9c02b3bb5bbcccf57ef9605d410d")
GITEE_REDIRECT_URI = os.getenv("GITEE_REDIRECT_URI", "http://localhost:3000/auth/gitee/callback")

GITEE_AUTH_URL = "https://gitee.com/oauth/authorize"
GITEE_TOKEN_URL = "https://gitee.com/oauth/token"
GITEE_USER_API = "https://gitee.com/api/v5/user"
