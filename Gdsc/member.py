import streamlit as st
import mysql.connector
import streamlit_authenticator as stauth
from signup import sign_up, fetch_users


db_config = {
    "host": "localhost",
    "user": "root",
    "password": " ",
    "database": "gdsc_data"
}


connection = mysql.connector.connect(**db_config)

# Create a cursor object
cursor = connection.cursor()

def main():
    try:
        users = fetch_users()
        emails = []
        usernames = []
        passwords = []

        for user in users:
            emails.append(user['key'])
            usernames.append(user['username'])
            passwords.append(user['password'])

        credentials = {'usernames': {}}
        for index in range(len(emails)):
            credentials['usernames'][usernames[index]] = {'name': emails[index], 'password': passwords[index]}

        Authenticator = stauth.Authenticate(credentials, cookie_name='Streamlit', key='abcdef', cookie_expiry_days=4)

        email, authentication_status, username = Authenticator.login(':green[Login]', 'main')

        info, info1 = st.columns(2)

        if not authentication_status:
            sign_up()

        if username:
            if username in usernames:
                if authentication_status:
                    # let User see app
                    st.sidebar.subheader(f'Welcome {username}')
                    Authenticator.logout('Log Out', 'sidebar')
                    member_entry()

                elif not authentication_status:
                    with info:
                        st.error('Incorrect Password or username')
                else:
                    with info:
                        st.warning('Please feed in your credentials')
            else:
                with info:
                    st.warning('Username does not exist, Please Sign up')

    except:
        st.success("Page refresh")


def member_entry():
    st.header("Member Entry Details")
    id_num = st.text_input("ID Number:")
    name = st.text_input("Name: ")
    r_no = st.text_input("Roll Number: ")
    ph_no = st.text_input("Phone Number: ")
    email = st.text_input("Email Id: ")
    year = st.text_input("Year & College :")
    branch = st.text_input("Branch: ")
    desig = st.text_input("Designation: ")
    team = st.selectbox("Choose Domain",['Android Domain', 'Cloud Domain', 'Competitive Coding Domain', 'Flutter Domain','Machine Learning Domain', 'Web Development Domain', 'Management Domain', 'Design Domain', 'Social Media Domain', 'Marketing Domain', 'Content Writing Domain', 'Data Management Domain' ])


    if st.button("Add"):
        insert_query = "INSERT INTO members (m_id, name, roll_number, p_no, email, year, branch, desig, db_name) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        values = (id_num, name, r_no, ph_no, email, year, branch, desig, team)
        cursor.execute(insert_query, values)
        connection.commit()
        st.success("Member Added Successfully!!")
