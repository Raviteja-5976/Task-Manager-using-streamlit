import streamlit as st
import streamlit_authenticator as stauth
import datetime
import re
from deta import Deta

DETA_KEY = 'Deta APi Key'

deta = Deta(DETA_KEY)

db = deta.Base('social_auth')

def fetch_users():
    """
    Fetch Users
    :return Dictionary of Users:
    """
    users = db.fetch()
    return users.items
