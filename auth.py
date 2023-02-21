# 1) Log-in --> https://chat.openai.com/chat
# 2) https://chat.openai.com/api/auth/session --> Go to this website and copy everything, then paste it to the "session_info" variable in "session_info.py" file. (e.g. session_info = {'user': 'user info', 'expires': 'expiration date', 'accessToken': 'token info'})

from session_info import session_info

# Processing
auth_config = session_info.get("accessToken")
assert auth_config is not None, "accessToken can not be empty."
auth_config = {"access_token": auth_config}