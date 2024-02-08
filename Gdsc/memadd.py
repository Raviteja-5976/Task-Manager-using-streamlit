import streamlit as st
import mysql.connector

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "Raviteja@5312",
    "database": "gdsc_data"
}


connection = mysql.connector.connect(**db_config)

# Create a cursor object
cursor = connection.cursor()

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
    domain = st.selectbox("Choose Domain",['Android Team', 'Cloud Team', 'Competitive Coding Team', 'Flutter Team','Machine Learning Team', 'Web Development Team', 'Management Team', 'Design Team', 'Social Media Team', 'Marketing Team', 'Content Writing Team', 'Data Management Team' ])


    if st.button("Add"):
        insert_query = "INSERT INTO members (m_id, name, roll_number, p_no, email, year, branch, desig, db_name) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        values = (id_num, name, r_no, ph_no, email, year, branch, desig, domain)
        cursor.execute(insert_query, values)
        connection.commit()
        st.success("Member Added Successfully!!")

if __name__ == "__main__":
        member_entry()