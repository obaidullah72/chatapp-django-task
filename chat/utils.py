# chat/utils.py
from .consumers import ONLINE_USERS

def is_user_online(user_id):
    return user_id in ONLINE_USERS
