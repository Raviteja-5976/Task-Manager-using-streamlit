import streamlit as st
import streamlit_authenticator as stauth
import datetime
import re
from deta import Deta

DETA_KEY = 'a0cohums9s2_bm9R1wGfrXU5F4EpqCqMVM14WHVd3UYG'

deta = Deta(DETA_KEY)

db = deta.Base('flu_auth')

def fetch_users():
    """
    Fetch Users
    :return Dictionary of Users:
    """
    users = db.fetch()
    return users.items