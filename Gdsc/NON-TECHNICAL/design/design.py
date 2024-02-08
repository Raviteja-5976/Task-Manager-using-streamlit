import streamlit as st
import mysql.connector
import streamlit_authenticator as stauth
from degauth import fetch_users


db_config = {
    "host": "localhost",
    "user": "root",
    "password": "Raviteja@5312",
    "database": "gdsc_data"
}

# Establish the connection
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

        Authenticator = stauth.Authenticate(credentials, cookie_name='Streamlit', key='abcdef', cookie_expiry_days=1)

        email, authentication_status, username = Authenticator.login(':green[Login]', 'main')

        info, info1 = st.columns(2)

        if username:
            if username in usernames:
                if authentication_status:
                    # let User see app
                    st.sidebar.subheader(f'Welcome {username}')
                    Authenticator.logout('Log Out', 'sidebar')
                    min()

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
        min()
    


def min():

    st.title("GDSC DESIGN DOMAIN")
    page = st.sidebar.selectbox("Select a page", ["Events", "Task Sheet", "Member Details", "Work Status"])
    
    if page == "Events":
        event()

    elif page == "Task Sheet":
        task()

    elif page == "Member Details":
        details()

    elif page == "Work Status":
        stat()


def event():
    from_date = st.date_input("From Date: ")
    to_date = st.date_input("To Date: ")
    sh_query = """
        select id, ev_name, gp_a, ev_date, ev_stat, ev_com from event 
        WHERE (%s IS NULL OR ev_date >= %s) AND ( %s IS NULL OR ev_date <= %s)
        ORDER BY ev_date DESC
        """
    sh_val =  (from_date, from_date, to_date, to_date)
    cursor.execute(sh_query,sh_val)
    ev_det = cursor.fetchall()

    st.subheader("Events")
    for ev in ev_det :
            st.write(f"Event: {ev[1]}")
            st.write(f'Affiliated Domains: {ev[2]}')
            st.write(f'Date: {ev[3]}')
            st.write(f'Status: {ev[4]}')
            st.write(f'Comment: {ev[5]}')

            if st.checkbox('Update Comment', key=f"edit_{ev[0]}"):
                edit_com = st.text_area("Edit Comment", ev[5])
                if st.button("Update Event"):
                    up_ev = '''
                    UPDATE event
                    SET ev_com = %s
                    WHERE id = %s
                    '''
                    up_values = (edit_com, ev[0])
                    cursor.execute(up_ev, up_values)
                    connection.commit()
                    st.success('Event Updated Successfully!!')
            st.write('-' * 50)
def task():
    st.subheader("Add Task")
    member_names_query = """
        SELECT m_id, name FROM members where db_name= "Design Team"
        """
    cursor.execute(member_names_query)
    member_names = cursor.fetchall()
    member_name = st.selectbox("Select Member", [f"{member[0]} - {member[1]}" for member in member_names])
    selected_m_id = member_name.split(' - ')[0] 
   
    name_t = st.text_input("Name of Task")
    assn_on = st.date_input("Assigned On")
    status = st.selectbox("Status", ["To-Do", "Progressing", "Completed"])
    com_on = st.date_input("Completed On")
    comment = st.text_area("Comment")
    if st.button("Add Task"):
        task_insert_query = "INSERT INTO task (member_id, do_name, name_t, assig_on, status, comp_on, comment) VALUES (%s,%s,%s,%s,%s,%s,%s) "
        ts_values = (selected_m_id, "Design Team", name_t, assn_on, status, com_on, comment)
        cursor.execute(task_insert_query, ts_values)
        connection.commit()
        st.success("Task Added Successfully !!")

   

def details():
    st.header("Details & Tasks")
    member_names_query = """
        SELECT m_id, name FROM members where db_name = "Design Team"
    """
    cursor.execute(member_names_query)
    member_names = cursor.fetchall()
    member_name = st.selectbox("Select Member", [f"{member[0]} - {member[1]}" for member in member_names])

    member_details_query = "SELECT m_id, name, roll_number, p_no, email, year, branch, desig FROM members WHERE m_id = %s "
    cursor.execute(member_details_query, (member_name.split(" - ")[0],))
    member_details = cursor.fetchone()

    st.subheader("Member Details")
    st.write(f"ID Number: {member_details[0]}")
    st.write(f"Name: {member_details[1]}")
    st.write(f"Roll Number: {member_details[2]}")
    st.write(f"Phone Number: {member_details[3]}")
    st.write(f"Email: {member_details[4]}")
    st.write(f"Year: {member_details[5]}")
    st.write(f"Branch: {member_details[6]}")
    st.write(f"Designation: {member_details[7]}")

    edit_member = st.checkbox('Edit Member Details')
    if edit_member:
        edit_name = st.text_input("Name:", member_details[1])
        edit_roll_number = st.text_input("Roll Number:", member_details[2])
        edit_phone_number = st.text_input("Phone Number:", member_details[3])
        edit_email = st.text_input("Email:", member_details[4])
        edit_year = st.text_input("Year:", value=member_details[5])
        edit_branch = st.text_input("Branch:", member_details[6])
        edit_designation = st.text_input("Designation:", member_details[7])
        
        
        if st.button("Update"):
            update_query = '''
                UPDATE members
                SET name = %s, roll_number = %s, p_no = %s, email = %s, year = %s, branch = %s, desig = %s
                WHERE m_id = %s
            '''
            update_values = (edit_name, edit_roll_number, edit_phone_number, edit_email, edit_year, edit_branch, edit_designation, member_details[0])
            cursor.execute(update_query, update_values)
            connection.commit()
            st.success("Updated Successfully!")

    # edit_member = st.checkbox('Edit Member Details')
    # if edit_member:
    #     # ... (your existing code for editing member details)

    from_date = st.date_input("From Date", key=None)
    to_date = st.date_input("To Date", key=None)

    if from_date is None and to_date is None:
        task_q = '''
            SELECT id, name_t, assig_on, status, comp_on, comment
            FROM task
            WHERE member_id = %s
        '''
        task_v = (member_details[0])
        cursor.execute(task_q, task_v)
        task_det = cursor.fetchall()  # Use fetchall() instead of fetchone()

    else:
        task_q = '''
            SELECT id, name_t, assig_on, status, comp_on, comment
            FROM task
            WHERE member_id = %s AND (%s IS NULL OR assig_on >= %s) AND (%s IS NULL OR assig_on <= %s)
        '''
        task_v = (member_details[0], from_date, from_date, to_date, to_date)
        cursor.execute(task_q, task_v)
        task_det = cursor.fetchall()  # Use fetchall() instead of fetchone()

    st.subheader(f"Tasks for {member_details[1]}")
    for task in task_det:
        st.write(f"Task: {task[1]}")
        st.write(f"Assigned On: {task[2]}")
        st.write(f"Status: {task[3]}")
        st.write(f"Completed On: {task[4]}")
        st.write(f"Comment: {task[5]}")
        

        if st.checkbox("Edit Task", key=f"edit_{task[0]}"):
            edit_t_name = st.text_input("Edit Task :",task[1])
            edit_status = st.selectbox("Edit Status",["To-Do", "Progressing", "Completed"])
            edit_comp_on = st.date_input("Completed On", task[4] if task[3] == "Completed" else None)
            edit_comment =  st.text_area("Edit Commemt :", task[5])

            if st.button("Update Task"):
                update_task ='''
                UPDATE task
                SET name_t = %s, status = %s, comp_on = %s, comment = %s 
                WHERE id = %s AND member_id = %s
                '''
                task_values = (edit_t_name, edit_status, edit_comp_on, edit_comment, task[0], member_details[0])

                cursor.execute(update_task, task_values)
                connection.commit()
                st.success("Task Updated Sucessfully")

        if st.checkbox("Delete Task", key=f"delete_{task[0]}"):
          if st.button("Confirm Delete"):
            delete_task_query = '''
            DELETE FROM task
            WHERE id = %s AND member_id = %s
            '''
            delete_task_values = (task[0], member_details[0])
            cursor.execute(delete_task_query, delete_task_values)
            connection.commit()
            st.success("Task Deleted Successfully")

        st.write("-" * 50)
        # if edit_task:


def stat():
    tab1, tab2, tab3 = st.tabs(["TO-DO","Progressing","Completed"])


    with tab1:
        to_query = '''
        SELECT member_id, name_t, assig_on, status, comp_on, comment
        FROM task
        WHERE status = "To-Do" AND do_name = "Design Team"
        ORDER BY assig_on DESC
        '''
        cursor.execute(to_query)
        to_det = cursor.fetchall()
    

        st.subheader("To-Do Tasks by Team")
        for to in to_det:

            mem = '''
            SELECT name from members WHERE m_id = %s
            '''

            cursor.execute(mem, (to[0], ))
            memb = cursor.fetchone()[0]    

            st.write(f"Member ID: {to[0]}")
            st.write(f"Name : {memb}")
            st.write(f"Task Name: {to[1]}")
            st.write(f"Assigned On: {to[2]}")
            st.write(f"Status: {to[3]}")
            st.write(f"Complete On: {to[4]}")
            st.write(f"Comment {to[5]}")

            st.write('-' * 50)

    with tab2: 
        pr_query = '''
        SELECT member_id, name_t, assig_on, status, comp_on, comment
        FROM task
        WHERE status = "Progressing" AND do_name = "Design Team"
        ORDER BY assig_on DESC
        '''
        cursor.execute(pr_query)
        pr_det = cursor.fetchall()


        st.subheader("Progressing Tasks by Team")
        for pr in pr_det:

            prm = '''
            SELECT name from members WHERE m_id = %s
            '''

            cursor.execute(prm, (pr[0],))  
            prm_m = cursor.fetchone()[0]         
            st.write(f"Member ID: {pr[0]}")
            st.write(f"Name : {prm_m}")            
            st.write(f"Task Name: {pr[1]}")
            st.write(f"Assigned On: {pr[2]}")
            st.write(f"Status: {pr[3]}")
            st.write(f"Complete On: {pr[4]}")
            st.write(f"Comment {pr[5]}")

            st.write('-' * 50)

    with tab3:
        co_query = '''
        SELECT member_id, name_t, assig_on, status, comp_on, comment
        FROM task
        WHERE status = "Completed" AND do_name = "Design Team"
        ORDER BY assig_on DESC
        '''
        cursor.execute(co_query)
        co_det = cursor.fetchall()


        st.subheader("Completed Tasks by Team")
        for co in co_det:

            com = '''
            SELECT name from members WHERE m_id = %s
            '''

            cursor.execute(com, (co[0],))  
            com_m = cursor.fetchone()[0]              
            st.write(f"Member ID: {co[0]}")
            st.write(f"Name: {com_m}")
            st.write(f"Task Name: {co[1]}")
            st.write(f"Assigned On: {co[2]}")
            st.write(f"Status: {co[3]}")
            st.write(f"Complete On: {co[4]}")
            st.write(f"Comment {co[5]}")


            st.write('-' * 50)

if __name__ == "__main__":
        main()
