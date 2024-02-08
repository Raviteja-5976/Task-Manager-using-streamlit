# This page is for the leads to monitor the progress in all the domains
import streamlit as st
import mysql.connector

db_config = {
    "host": "Host_name",
    "user": "User_name",
    "password": "Password",
    "database": "Database_name"
}

# Establish the connection
connection = mysql.connector.connect(**db_config)

# Create a cursor object
cursor = connection.cursor()


def main():
    st.title('GDSC Lead Page')
    page = st.sidebar.selectbox('Select Box', ['Events','Events Stat','Show Tasks'])
    if page == 'Events' :
        adev()

    elif page == 'Events Stat':
         evstst()
    
    elif page == 'Show Tasks':
          shta()

def adev():
    st.subheader('Events of GDSC')



    en = st.text_input('Event Name')
    gp = st.text_input('Affiliated Domains')
    ed = st.date_input('Event Date')
    sa = st.selectbox('Status', ['Future Event','On going','Completed'])
    com = st.text_area('Comment')
    if st.button('Add Event'):
        ev_query = """
        INSERT INTO event (ev_name, gp_a, ev_date, ev_stat, ev_com) VALUES (%s,%s,%s,%s,%s)
        """
        ev_values = (en , gp , ed, sa , com)
        cursor.execute(ev_query, ev_values)
        connection.commit()
        st.success('Event Added Successfully !!')

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

            if st.checkbox('Edit Event', key=f"edit_{ev[0]}"):
                edit_en = st.text_input("Edit Event Name : ",ev[1])
                edit_gp = st.text_input("Edit Afffiliated Domains: ",ev[2])
                edit_ed = st.date_input("Edit Event Date",ev[3])
                edit_sa = st.selectbox("Edit Status", ['Future Event','On going', 'Completed'])
                edit_com = st.text_area("Edit Comment", ev[5])
            

                if st.button("Update Event"):
                    up_ev = '''
                    UPDATE event
                    SET ev_name = %s, gp_a = %s, ev_date = %s, ev_stat = %s, ev_com = %s
                    '''
                    up_values = (edit_en, edit_gp, edit_ed, edit_sa, edit_com)
                    cursor.execute(up_ev, up_values)
                    connection.commit()
                    st.success('Event Updated Successfully!!')
            if st.checkbox("Delete Event", key=f"delete_{ev[0]}"):
                 if st.button("Confirm Delete"):
                    delete_ev = '''
                    DELETE FROM event
                    WHERE id = %s
                    '''
                    delete_val = (ev[0])
                    cursor.execute(delete_ev, (delete_val, ))
                    connection.commit()
                    st.success("Event Deleted Successfully !!")
            st.write('-' * 50)

def evstst():
     tab_1, tab_2, tab_3 = st.tabs(['Future Event',' On going','Completed'])

     with tab_1:
          fe_query = '''
            SELECT ev_name, gp_a, ev_date, ev_stat, ev_com from event
            WHERE ev_stat = 'Future Event'
            ORDER BY ev_date DESC
            '''
          cursor.execute(fe_query)
          fe_det = cursor.fetchall()
          
          st.subheader("Future Events")
          for fe in fe_det :
               st.write(f"Event : {fe[0]}")
               st.write(f"Affiliated Domains : {fe[1]}")
               st.write(f"Date : {fe[2]}")
               st.write(f"Status : {fe[3]}")
               st.write(f"Comment : {fe[4]}")

               st.write('-' * 50)

     with tab_2:
        fe_query = '''
        SELECT ev_name, gp_a, ev_date, ev_stat, ev_com from event
        WHERE ev_stat = 'On going'
        ORDER BY ev_date DESC
        '''
        cursor.execute(fe_query)
        fe_det = cursor.fetchall()
        
        st.subheader("on Going Events")
        for fe in fe_det :
            st.write(f"Event : {fe[0]}")
            st.write(f"Affiliated Domains : {fe[1]}")
            st.write(f"Date : {fe[2]}")
            st.write(f"Status : {fe[3]}")
            st.write(f"Comment : {fe[4]}")

            st.write('-' * 50)


     with tab_3:
        fe_query = '''
        SELECT ev_name, gp_a, ev_date, ev_stat, ev_com from event
        WHERE ev_stat = 'Completed'
        ORDER BY ev_date DESC
        '''
        cursor.execute(fe_query)
        fe_det = cursor.fetchall()
        
        st.subheader("Completed Events")
        for fe in fe_det :
            st.write(f"Event : {fe[0]}")
            st.write(f"Affiliated Domains : {fe[1]}")
            st.write(f"Date : {fe[2]}")
            st.write(f"Status : {fe[3]}")
            st.write(f"Comment : {fe[4]}")

            st.write('-' * 50)

def shta():

    sedm = st.selectbox('Select Domain', ['Android Team', 'Cloud Team', 'Competitive Coding Team', 'Flutter Team','Machine Learning Team', 'Web Development Team', 'Management Team', 'Design Team', 'Social Media Team', 'Marketing Team', 'Content Writing Team', 'Data Management Team' ])

    tab1, tab2, tab3 = st.tabs(['To-Do', 'Progressing', 'Completed'])
    
    with tab1:
        to_query = '''
        SELECT member_id, name_t, assig_on, status, comp_on, comment
        FROM task
        WHERE status = "To-Do" AND do_name = %s
        '''

        cursor.execute(to_query, (sedm,))
        to_det = cursor.fetchall()
    

        st.subheader("To-Do Tasks by Team")
        for to in to_det:

            mem = '''
            SELECT name from members WHERE m_id = %s
            '''

            cursor.execute(mem, (to[0], ))
            memb = cursor.fetchone()[0]    

            st.write(f"Member ID:  {to[0]}")
            st.write(f"Name :  {memb}")
            st.write(f"Task Name:  {to[1]}")
            st.write(f"Assigned On:  {to[2]}")
            st.write(f"Status:  {to[3]}")
            st.write(f"Complete On:  {to[4]}")
            st.write(f"Comment:  {to[5]}")

            st.write('-' * 50)

    with tab2: 
        pr_query = '''
        SELECT member_id, name_t, assig_on, status, comp_on, comment
        FROM task
        WHERE status = "Progressing" AND do_name = %s
        '''

        cursor.execute(pr_query, (sedm,))
        pr_det = cursor.fetchall()


        st.subheader("Progressing Tasks by Team")
        for pr in pr_det:

            prm = '''
            SELECT name from members WHERE m_id = %s
            '''

            cursor.execute(prm, (pr[0],))  
            prm_m = cursor.fetchone()[0]         
            st.write(f"Member ID:  {pr[0]}")
            st.write(f"Name :  {prm_m}")            
            st.write(f"Task Name:  {pr[1]}")
            st.write(f"Assigned On:  {pr[2]}")
            st.write(f"Status:  {pr[3]}")
            st.write(f"Complete On:  {pr[4]}")
            st.write(f"Comment:  {pr[5]}")

            st.write('-' * 50)

    with tab3:
        co_query = '''
        SELECT member_id, name_t, assig_on, status, comp_on, comment
        FROM task
        WHERE status = "Completed" AND do_name = %s
        '''

        cursor.execute(co_query, (sedm,))
        co_det = cursor.fetchall()


        st.subheader("Completed Tasks by Team")
        for co in co_det:

            com = '''
            SELECT name from members WHERE m_id = %s
            '''

            cursor.execute(com, (co[0],))  
            com_m = cursor.fetchone()[0]              
            st.write(f"Member ID:  {co[0]}")
            st.write(f"Name:  {com_m}")
            st.write(f"Task Name:  {co[1]}")
            st.write(f"Assigned On:  {co[2]}")
            st.write(f"Status:  {co[3]}")
            st.write(f"Complete On:  {co[4]}")
            st.write(f"Comment:  {co[5]}")


            st.write('-' * 50)



if __name__ == "__main__":
        main()

            # tab1, tab2, tab3 = st.tabs(['Future Event'], ['On going'], ['Completed'])
    # with tab1 :
    #     fe_query = """
    #         select ev_name, gp_a, ev_date, ev_stat, ev_com from event where ev_stat = "Future Event" ORDER BY ev_date
    #         """
    #     cursor.execute(fe_query)
    #     fe_det = cursor.fetchall()

    #     st.subheader("Future Events")
    #     for fe in fe_det :
    #          st.write(f"Event: {fe[0]}")
    #          st.write(f'Affiliated Domains: {fe[1]}')
    #          st.write(f'Date: {fe[2]}')
    #          st.write(f'Status: {fe[3]}')
    #          st.write(f'Comment: {fe[4]}')
    #          st.write('-' * 50)
