import streamlit as st
import pandas as pd
import sqlite3
from database import (
    create_emp_table, 
    add_employee,
    get_employees,
    get_single_employees,
    update_employee,
    delete_epmloyee_data,    
)
# page config
st.set_page_config(
    page_title='Employee Management System',
    layout="wide", page_icon=":material/directions_boat:"
)

st.sidebar.header("Working with Sales Data")
# create table
create_emp_table()

st.title('Employee Management System')
st.write(
    "Employee Management System With complete Crud Operation using streamlit and Sqlite3"
)

menu = st.sidebar.selectbox(
    "Select Your Operation", 
    [
        "Create employee",
        "View Employees",
        "Update Employee",
        "Delete Employee"
    ]
)

if menu == "Create employee":
    st.header("+ Add New Employee Here..")
    with st.form('create employee form'):
        name = st.text_input("Enter Your Name", placeholder="Employee Name")
        email = st.text_input("enter Your Email", placeholder='Employee email address')
        department = st.selectbox(
            "Department",
            [
                "CSE",
                "EEC",
                "Banking",
                "Engineering",
                "Data Science",
                "Sales",
                "HR",
                "HOD"
            ],
            placeholder="Department"
        )
        salary = st.number_input(
            "Salary", min_value=0, max_value=120000, placeholder="Employee Salary"
        )
        submit = st.form_submit_button(
            "Add Employee"
        )

        if submit:
            if not name or not email:
                st.error(
                    "Name and Email are required"
                )
            else:
                try:
                    add_employee(
                        name, 
                        email,
                        department,
                        salary
                    )
                    st.success("Employee Addedd")
                except sqlite3.IntegrityError :
                    st.error("Email already Exists...")
elif menu == "View Employees":
    st.header("All employees Listed Here..")
    df  = get_employees()
    if df.empty:
        st.warning(
            "No Employee available"
        )
    else:
        search  = st.text_input('Search emp')
        if search:
            search_lower = search.lower()
            df = df[
                df['name'].str.lower().str.contains(search_lower, na=False) |
                df['department'].str.lower().str.contains(search_lower, na=False)
            ]
            # st.dataframe(df)

            # metrix
            col1, col2, col3 = st.columns(3)
            col1.metric(
                "Total Emloyee", len(df)
            )
            col2.metric(
                "Average Salary", f"{df['salary'].mean():.2f}"
            )
            col3.metric(
                "Total Salary", f"{df['salary'].sum():.2f}"
            )
        st.divider()
        # display data
        st.dataframe(df, width='stretch')

elif  menu == "Update Employee":
    st.header('Update employee Page')
    df = get_employees()

    if df.empty:
        st.warning('No emploee')
    else:
        emp_ids = df['id'].tolist()
        emp_id = st.selectbox("Select Emloyee Id", emp_ids)

        if emp_id:
            employee = get_single_employees(emp_id)

            if employee:
                epmloyee_id = employee[0]
                epmloyee_name = employee[1]
                epmloyee_email = employee[2]
                epmloyee_department = employee[3]
                epmloyee_salary = employee[4]
                # st.write(employee)
                
                departments = [
                        "CSE",
                        "EEC",
                        "Banking",
                        "Engineering",
                        "Data Science",
                        "Sales",
                        "HR",
                        "HOD"
                    ]
                current_index = departments.index(
                    epmloyee_department   
                )

                with st.form('update employee form'):
                    name = st.text_input("emp Name", value=epmloyee_name)
                    email = st.text_input("emp Emil", value=epmloyee_email)
                    department = st.selectbox("Select Dept", departments, index=current_index)
                    salary = st.number_input("emp Salary", min_value=0.0, value=float(epmloyee_salary), step=1000.0)
                    update_submit = (
                        st.form_submit_button("Update employee")
                    ) 

                    if update_submit:
                        try:
                            update_employee(
                                epmloyee_id, name, email, department, salary
                            )
                            st.success("Updated..")
                        except sqlite3.InternalError:
                            st.error("Email Already Exist")
elif menu == 'Delete Employee':
    st.header("Delete Employee ")
    df = get_employees()
    if df.empty:
        st.warning("No employee found")
    else:
        emp_ids = df['id'].tolist()
        emp_id = st.selectbox("Select Emloyee Id", emp_ids)

        employee = get_single_employees(emp_id)

        if employee:
            st.subheader("Selected Employee")

            col1, col2 = st.columns(2)
            col1.write(f"**Name : {employee[1]}")
            col2.write(f"**Email : {employee[2]}")

            st.write(f"**Department : {employee[3]}")
            st.write(f"**Salary : {employee[4]:0.2f}")

            confirm = st.checkbox(
                "confirm If You want to Delete the employee"
            )

            if confirm:
                if st.button("Delete Employee", type="primary",  ):
                    delete_epmloyee_data(emp_id)
                    st.success("employee Deleted..")
                    st.rerun()
                    