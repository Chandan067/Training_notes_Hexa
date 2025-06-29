from util.db_conn_util import get_connection
from entity.employee import Employee
from datetime import date
from exceptions.custom_exceptions import (
    EmployeeNotFoundException,
    InvalidInputException,
    DatabaseConnectionException
)

class EmployeeService:
    def add_employee(self, emp: Employee):
        conn = None
        cursor = None
        try:
            # Extra safety validation in case input validator is skipped
            if not emp.first_name or not emp.last_name or not emp.first_name.strip() or not emp.last_name.strip():
                raise InvalidInputException("First and Last Name cannot be empty.")

            conn = get_connection()
            cursor = conn.cursor()
            query = """
            INSERT INTO employee 
            (first_name, last_name, DoB, gender, email, phno, address, designation, join_date, exit_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            data = (
                emp.first_name.strip(), emp.last_name.strip(), emp.dob, emp.gender.strip(), emp.email.strip(),
                emp.phone.strip(), emp.address.strip(), emp.position.strip(), emp.join_date, emp.termination_date
            )
            cursor.execute(query, data)
            conn.commit()
            print("✅ Employee added successfully!")
        except (InvalidInputException, EmployeeNotFoundException) as e:
            raise
        except Exception as e:
            raise DatabaseConnectionException(f"Failed to add employee: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_all_employees(self):
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            query = "SELECT * FROM employee"
            cursor.execute(query)
            rows = cursor.fetchall()

            if rows:
                print("\n📋 All Employees:")
                for row in rows:
                    print(f"ID: {row[0]}, Name: {row[1]} {row[2]}, Email: {row[5]}, Designation: {row[8]}")
            else:
                print("No employee records found.")
        except Exception as e:
            raise DatabaseConnectionException(f"Failed to fetch employees: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_employee_by_id(self, emp_id):
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            query = "SELECT * FROM employee WHERE employee_id = %s"
            cursor.execute(query, (emp_id,))
            row = cursor.fetchone()

            if not row:
                raise EmployeeNotFoundException(f"Employee with ID {emp_id} not found.")

            dob = row[3]
            age_text = "N/A"
            if dob:
                try:
                    today = date.today()
                    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
                    age_text = f"{age} years"
                except Exception as e:
                    age_text = f"Error calculating age: {e}"

            print("\n👤 Employee Details:")
            print(f"ID: {row[0]}")
            print(f"Name: {row[1]} {row[2]}")
            print(f"DoB: {dob} (Age: {age_text}), Gender: {row[4]}")
            print(f"Email: {row[5]}, Phone: {row[6]}")
            print(f"Address: {row[7]}, Designation: {row[8]}")
            print(f"Join Date: {row[9]}, Exit Date: {row[10]}")
        except EmployeeNotFoundException as e:
            raise
        except Exception as e:
            raise DatabaseConnectionException(f"Failed to retrieve employee: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def update_employee(self, emp_id, updated_emp: Employee):
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM employee WHERE employee_id = %s", (emp_id,))
            if not cursor.fetchone():
                raise EmployeeNotFoundException(f"Employee with ID {emp_id} not found.")

            query = """
            UPDATE employee
            SET first_name = %s,
                last_name = %s,
                DoB = %s,
                gender = %s,
                email = %s,
                phno = %s,
                address = %s,
                designation = %s,
                join_date = %s,
                exit_date = %s
            WHERE employee_id = %s
            """

            data = (
                updated_emp.first_name.strip(), updated_emp.last_name.strip(), updated_emp.dob,
                updated_emp.gender.strip(), updated_emp.email.strip(), updated_emp.phone.strip(),
                updated_emp.address.strip(), updated_emp.position.strip(),
                updated_emp.join_date, updated_emp.termination_date, emp_id
            )

            cursor.execute(query, data)
            conn.commit()
            print(f"✅ Employee ID {emp_id} updated successfully.")
        except EmployeeNotFoundException as e:
            raise
        except Exception as e:
            raise DatabaseConnectionException(f"Failed to update employee: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def delete_employee(self, emp_id):
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM employee WHERE employee_id = %s", (emp_id,))
            if not cursor.fetchone():
                raise EmployeeNotFoundException(f"Employee with ID {emp_id} not found.")

            query = "DELETE FROM employee WHERE employee_id = %s"
            cursor.execute(query, (emp_id,))
            conn.commit()
            print(f"✅ Employee ID {emp_id} deleted successfully.")
        except EmployeeNotFoundException as e:
            raise
        except Exception as e:
            raise DatabaseConnectionException(f"Failed to delete employee: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
