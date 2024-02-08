import streamlit as st
import streamlit_authenticator as stauth
import datetime
import re
from deta import Deta

DETA_KEY = 'a0cohums9s2_HSyScoV7PPwmhcBvBtukH38H2rXm7SKq'

deta = Deta(DETA_KEY)

db = deta.Base('member_details')

def fetch_users():
    """
    Fetch Users
    :return Dictionary of Users:
    """
    users = db.fetch()
    return users.items