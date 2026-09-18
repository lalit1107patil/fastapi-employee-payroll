import streamlit as st
import requests
from datetime import date

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Employee Payroll Management",
    page_icon="💼",
    layout="wide"
)

st.title("💼 Employee & Payroll Management System")
st.caption("FastAPI + PostgreSQL + Streamlit")

st.divider()

menu = st.sidebar.selectbox(
    "Select Module",
    ["Dashboard", "Departments", "Employees", "Payslips"]
)


# =========================================================
# DASHBOARD
# =========================================================

if menu == "Dashboard":

    st.header("📊 Dashboard")

    try:
        employees = requests.get(
            f"{API_URL}/employees/"
        ).json()

        departments = requests.get(
            f"{API_URL}/departments/"
        ).json()

        payslips = requests.get(
            f"{API_URL}/payslips/"
        ).json()

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "👨‍💼 Employees",
            len(employees)
        )

        col2.metric(
            "🏢 Departments",
            len(departments)
        )

        col3.metric(
            "💰 Payslips",
            len(payslips)
        )

    except requests.exceptions.RequestException:
        st.error("FastAPI server is not running.")


# =========================================================
# DEPARTMENTS
# =========================================================

elif menu == "Departments":

    st.header("🏢 Department Management")

    tab1, tab2, tab3 = st.tabs(
        ["View Departments", "Add Department", "Edit / Delete"]
    )

    # ---------------- VIEW ----------------

    with tab1:

        response = requests.get(
            f"{API_URL}/departments/"
        )

        if response.status_code == 200:

            departments = response.json()

            if not departments:
                st.info("No departments found.")

            for department in departments:

                st.subheader(
                    f"🏢 {department['name']}"
                )

                st.write(
                    f"👤 Manager: {department['manager_name']}"
                )

                st.write(
                    f"🆔 Department ID: {department['id']}"
                )

                st.divider()

        else:
            st.error(response.text)

    # ---------------- ADD ----------------

    with tab2:

        name = st.text_input(
            "Department Name",
            key="dept_add_name"
        )

        manager = st.text_input(
            "Manager Name",
            key="dept_add_manager"
        )

        if st.button(
            "➕ Add Department",
            key="add_department"
        ):

            if not name.strip():
                st.error("Department name cannot be blank.")

            elif not manager.strip():
                st.error("Manager name cannot be blank.")

            else:

                data = {
                    "name": name.strip(),
                    "manager_name": manager.strip()
                }

                response = requests.post(
                    f"{API_URL}/departments/",
                    json=data
                )

                if response.status_code == 201:
                    st.success(
                        "Department created successfully!"
                    )
                    st.rerun()

                else:
                    st.error(response.text)

    # ---------------- EDIT / DELETE ----------------

    with tab3:

        response = requests.get(
            f"{API_URL}/departments/"
        )

        if response.status_code == 200:

            departments = response.json()

            if departments:

                department_options = {
                    f"{d['id']} - {d['name']}": d
                    for d in departments
                }

                selected = st.selectbox(
                    "Select Department",
                    list(department_options.keys()),
                    key="dept_select"
                )

                department = department_options[selected]

                new_name = st.text_input(
                    "Department Name",
                    value=department["name"],
                    key="dept_edit_name"
                )

                new_manager = st.text_input(
                    "Manager Name",
                    value=department["manager_name"],
                    key="dept_edit_manager"
                )

                col1, col2 = st.columns(2)

                with col1:

                    if st.button(
                        "✏️ Update Department",
                        key="update_department"
                    ):

                        if not new_name.strip():
                            st.error(
                                "Department name cannot be blank."
                            )

                        elif not new_manager.strip():
                            st.error(
                                "Manager name cannot be blank."
                            )

                        else:

                            data = {
                                "name": new_name.strip(),
                                "manager_name": new_manager.strip()
                            }

                            response = requests.put(
                                f"{API_URL}/departments/{department['id']}",
                                json=data
                            )

                            if response.status_code == 200:
                                st.success(
                                    "Department updated successfully!"
                                )
                                st.rerun()

                            else:
                                st.error(response.text)

                with col2:

                    if st.button(
                        "🗑️ Delete Department",
                        key="delete_department"
                    ):

                        response = requests.delete(
                            f"{API_URL}/departments/{department['id']}"
                        )

                        if response.status_code == 200:
                            st.success(
                                "Department deleted successfully!"
                            )
                            st.rerun()

                        else:
                            st.error(response.text)

            else:
                st.info("No departments available.")


# =========================================================
# EMPLOYEES
# =========================================================

elif menu == "Employees":

    st.header("👨‍💼 Employee Management")

    tab1, tab2, tab3 = st.tabs(
        ["View Employees", "Add Employee", "Edit / Delete"]
    )

    # ---------------- VIEW ----------------

    with tab1:

        response = requests.get(
            f"{API_URL}/employees/"
        )

        if response.status_code == 200:

            employees = response.json()

            if not employees:
                st.info("No employees found.")

            for employee in employees:

                st.subheader(
                    f"👨‍💼 {employee['name']}"
                )

                col1, col2 = st.columns(2)

                with col1:

                    st.write(
                        f"🆔 ID: {employee['id']}"
                    )

                    st.write(
                        f"📧 Email: {employee['email']}"
                    )

                    st.write(
                        f"📱 Phone: {employee['phone']}"
                    )

                with col2:

                    st.write(
                        f"💰 Salary: ₹{employee['salary']}"
                    )

                    st.write(
                        f"📅 Joining Date: {employee['joining_date']}"
                    )

                    st.write(
                        f"🏢 Department ID: "
                        f"{employee['department_id']}"
                    )

                st.divider()

        else:
            st.error(response.text)

    # ---------------- ADD ----------------

    with tab2:

        name = st.text_input(
            "Employee Name",
            key="emp_add_name"
        )

        email = st.text_input(
            "Email",
            key="emp_add_email"
        )

        phone = st.text_input(
            "Phone",
            key="emp_add_phone"
        )

        salary = st.number_input(
            "Salary",
            min_value=0.0,
            step=1000.0,
            key="emp_add_salary"
        )

        joining_date = st.date_input(
            "Joining Date",
            value=date.today(),
            key="emp_add_date"
        )

        department_id = st.number_input(
            "Department ID",
            min_value=1,
            step=1,
            key="emp_add_department"
        )

        if st.button(
            "➕ Add Employee",
            key="add_employee"
        ):

            if not name.strip():
                st.error("Employee name cannot be blank.")

            elif not email.strip():
                st.error("Email cannot be blank.")

            elif not phone.strip():
                st.error("Phone cannot be blank.")

            elif salary <= 0:
                st.error("Salary must be greater than 0.")

            else:

                data = {
                    "name": name.strip(),
                    "email": email.strip(),
                    "phone": phone.strip(),
                    "salary": salary,
                    "joining_date": str(joining_date),
                    "department_id": department_id
                }

                response = requests.post(
                    f"{API_URL}/employees/",
                    json=data
                )

                if response.status_code == 201:
                    st.success(
                        "Employee created successfully!"
                    )
                    st.rerun()

                else:
                    st.error(response.text)

    # ---------------- EDIT / DELETE ----------------

    with tab3:

        response = requests.get(
            f"{API_URL}/employees/"
        )

        if response.status_code == 200:

            employees = response.json()

            if employees:

                employee_options = {
                    f"{e['id']} - {e['name']}": e
                    for e in employees
                }

                selected = st.selectbox(
                    "Select Employee",
                    list(employee_options.keys()),
                    key="emp_select"
                )

                employee = employee_options[selected]

                new_name = st.text_input(
                    "Name",
                    value=employee["name"],
                    key="emp_edit_name"
                )

                new_email = st.text_input(
                    "Email",
                    value=employee["email"],
                    key="emp_edit_email"
                )

                new_phone = st.text_input(
                    "Phone",
                    value=employee["phone"] or "",
                    key="emp_edit_phone"
                )

                new_salary = st.number_input(
                    "Salary",
                    min_value=0.0,
                    value=float(employee["salary"]),
                    step=1000.0,
                    key="emp_edit_salary"
                )

                new_date = st.date_input(
                    "Joining Date",
                    value=date.fromisoformat(
                        employee["joining_date"]
                    ),
                    key="emp_edit_date"
                )

                new_department = st.number_input(
                    "Department ID",
                    min_value=1,
                    value=employee["department_id"] or 1,
                    step=1,
                    key="emp_edit_department"
                )

                col1, col2 = st.columns(2)

                with col1:

                    if st.button(
                        "✏️ Update Employee",
                        key="update_employee"
                    ):

                        if not new_name.strip():
                            st.error(
                                "Employee name cannot be blank."
                            )

                        elif not new_email.strip():
                            st.error(
                                "Email cannot be blank."
                            )

                        elif not new_phone.strip():
                            st.error(
                                "Phone cannot be blank."
                            )

                        elif new_salary <= 0:
                            st.error(
                                "Salary must be greater than 0."
                            )

                        else:

                            data = {
                                "name": new_name.strip(),
                                "email": new_email.strip(),
                                "phone": new_phone.strip(),
                                "salary": new_salary,
                                "joining_date": str(new_date),
                                "department_id": new_department
                            }

                            response = requests.put(
                                f"{API_URL}/employees/{employee['id']}",
                                json=data
                            )

                            if response.status_code == 200:
                                st.success(
                                    "Employee updated successfully!"
                                )
                                st.rerun()

                            else:
                                st.error(response.text)

                with col2:

                    if st.button(
                        "🗑️ Delete Employee",
                        key="delete_employee"
                    ):

                        response = requests.delete(
                            f"{API_URL}/employees/{employee['id']}"
                        )

                        if response.status_code == 200:
                            st.success(
                                "Employee deleted successfully!"
                            )
                            st.rerun()

                        else:
                            st.error(response.text)

            else:
                st.info("No employees available.")


# =========================================================
# PAYSLIPS
# =========================================================

elif menu == "Payslips":

    st.header("💰 Payroll Management")

    tab1, tab2, tab3 = st.tabs(
        ["View Payslips", "Generate Payslip", "Edit / Delete"]
    )

    # ---------------- VIEW ----------------

    with tab1:

        response = requests.get(
            f"{API_URL}/payslips/"
        )

        if response.status_code == 200:

            payslips = response.json()

            if not payslips:
                st.info("No payslips found.")

            for payslip in payslips:

                st.subheader(
                    f"💰 Payslip #{payslip['id']}"
                )

                col1, col2, col3 = st.columns(3)

                with col1:

                    st.write(
                        f"👨‍💼 Employee: "
                        f"{payslip['employee_name']}"
                    )

                    st.write(
                        f"📅 Month: "
                        f"{payslip['month']} / "
                        f"{payslip['year']}"
                    )

                with col2:

                    st.write(
                        f"💵 Basic Salary: "
                        f"₹{payslip['basic_salary']}"
                    )

                    st.write(
                        f"➖ Deductions: "
                        f"₹{payslip['deductions']}"
                    )

                with col3:

                    st.write(
                        f"💰 Net Pay: "
                        f"₹{payslip['net_pay']}"
                    )

                st.divider()

        else:
            st.error(response.text)

    # ---------------- GENERATE ----------------

    with tab2:

        employee_response = requests.get(
            f"{API_URL}/employees/"
        )

        if employee_response.status_code == 200:

            employees = employee_response.json()

            if employees:

                employee_options = {
                    f"{e['id']} - {e['name']}": e
                    for e in employees
                }

                selected_employee = st.selectbox(
                    "Select Employee",
                    list(employee_options.keys()),
                    key="payslip_employee"
                )

                employee = employee_options[
                    selected_employee
                ]

                month = st.number_input(
                    "Month",
                    min_value=1,
                    max_value=12,
                    value=1,
                    step=1,
                    key="payslip_month"
                )

                year = st.number_input(
                    "Year",
                    min_value=2000,
                    value=2026,
                    step=1,
                    key="payslip_year"
                )

                deductions = st.number_input(
                    "Deductions",
                    min_value=0.0,
                    value=0.0,
                    step=500.0,
                    key="payslip_deductions"
                )

                st.info(
                    f"Basic Salary: ₹{employee['salary']}"
                )

                if deductions > employee["salary"]:
                    st.error(
                        "Deductions cannot be greater than salary."
                    )

                if st.button(
                    "💳 Generate Payslip",
                    key="generate_payslip"
                ):

                    if deductions > employee["salary"]:
                        st.error(
                            "Deductions cannot be greater than salary."
                        )

                    else:

                        data = {
                            "month": month,
                            "year": year,
                            "deductions": deductions
                        }

                        response = requests.post(
                            f"{API_URL}/payslips/generate/"
                            f"{employee['id']}",
                            json=data
                        )

                        if response.status_code == 201:
                            st.success(
                                "Payslip generated successfully!"
                            )
                            st.rerun()

                        else:
                            st.error(response.text)

            else:
                st.warning(
                    "Create an employee first."
                )

    # ---------------- EDIT / DELETE ----------------

    with tab3:

        response = requests.get(
            f"{API_URL}/payslips/"
        )

        if response.status_code == 200:

            payslips = response.json()

            if payslips:

                payslip_options = {
                    f"#{p['id']} - "
                    f"{p['employee_name']} - "
                    f"{p['month']}/{p['year']}": p
                    for p in payslips
                }

                selected = st.selectbox(
                    "Select Payslip",
                    list(payslip_options.keys()),
                    key="payslip_select"
                )

                payslip = payslip_options[selected]

                if payslip["employee_id"] is None:

                    st.warning(
                        "This is a historical payslip. "
                        "The employee has been deleted, "
                        "so it cannot be edited."
                    )

                    if st.button(
                        "🗑️ Delete Payslip",
                        key="delete_historical_payslip"
                    ):

                        response = requests.delete(
                            f"{API_URL}/payslips/{payslip['id']}"
                        )

                        if response.status_code == 200:
                            st.success(
                                "Payslip deleted successfully!"
                            )
                            st.rerun()

                        else:
                            st.error(response.text)

                else:

                    new_month = st.number_input(
                        "Month",
                        min_value=1,
                        max_value=12,
                        value=payslip["month"],
                        step=1,
                        key="payslip_edit_month"
                    )

                    new_year = st.number_input(
                        "Year",
                        min_value=2000,
                        value=payslip["year"],
                        step=1,
                        key="payslip_edit_year"
                    )

                    new_deductions = st.number_input(
                        "Deductions",
                        min_value=0.0,
                        value=float(payslip["deductions"]),
                        step=500.0,
                        key="payslip_edit_deductions"
                    )

                    col1, col2 = st.columns(2)

                    with col1:

                        if st.button(
                            "✏️ Update Payslip",
                            key="update_payslip"
                        ):

                            data = {
                                "month": new_month,
                                "year": new_year,
                                "deductions": new_deductions
                            }

                            response = requests.put(
                                f"{API_URL}/payslips/{payslip['id']}",
                                json=data
                            )

                            if response.status_code == 200:
                                st.success(
                                    "Payslip updated successfully!"
                                )
                                st.rerun()

                            else:
                                st.error(response.text)

                    with col2:

                        if st.button(
                            "🗑️ Delete Payslip",
                            key="delete_payslip"
                        ):

                            response = requests.delete(
                                f"{API_URL}/payslips/{payslip['id']}"
                            )

                            if response.status_code == 200:
                                st.success(
                                    "Payslip deleted successfully!"
                                )
                                st.rerun()

                            else:
                                st.error(response.text)

            else:
                st.info("No payslips available.")