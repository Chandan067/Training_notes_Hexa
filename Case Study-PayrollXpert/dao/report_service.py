from util.db_conn_util import get_connection
from exceptions.custom_exceptions import (
    DatabaseConnectionException,
    InvalidInputException
)

class ReportService:

    def payroll_summary(self, min_salary=None):
        try:
            if min_salary is not None:
                if not isinstance(min_salary, (int, float)) or min_salary < 0:
                    raise InvalidInputException("Minimum salary filter must be a non-negative number.")

            conn = get_connection()
            cursor = conn.cursor()
            query = """
            SELECT e.employee_id, e.first_name, e.last_name, SUM(p.net_salary)
            FROM employee e
            JOIN payroll p ON e.employee_id = p.employee_id
            GROUP BY e.employee_id
            """
            if min_salary is not None:
                query += " HAVING SUM(p.net_salary) > %s"
                cursor.execute(query, (min_salary,))
            else:
                cursor.execute(query)

            rows = cursor.fetchall()
            cursor.close()
            conn.close()

            print("\n📊 Payroll Summary Report:")
            for row in rows:
                print(f"Employee ID: {row[0]}, Name: {row[1]} {row[2]}, Total Net Salary: ₹{row[3]}")

        except InvalidInputException as e:
            raise e
        except Exception as e:
            raise DatabaseConnectionException(f"❌ Error generating payroll summary: {e}")

    def tax_summary(self):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            query = """
            SELECT e.employee_id, e.first_name, e.last_name, SUM(t.tax_amount)
            FROM employee e
            JOIN tax t ON e.employee_id = t.employee_id
            GROUP BY e.employee_id
            """
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()
            conn.close()

            print("\n📊 Tax Summary Report:")
            for row in rows:
                print(f"Employee ID: {row[0]}, Name: {row[1]} {row[2]}, Total Tax Paid: ₹{row[3]}")

        except Exception as e:
            raise DatabaseConnectionException(f"❌ Error generating tax summary: {e}")

    def financial_summary(self):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            query = """
            SELECT employee_id, record_type, SUM(amount)
            FROM financial_record
            GROUP BY employee_id, record_type
            """
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()
            conn.close()

            print("\n📊 Financial Summary Report:")
            summary = {}
            for emp_id, rtype, total in rows:
                if emp_id not in summary:
                    summary[emp_id] = {"income": 0, "expense": 0}
                summary[emp_id][rtype] = total

            for emp_id, data in summary.items():
                income = data.get("income", 0)
                expense = data.get("expense", 0)
                print(f"Employee ID: {emp_id} | Total Income: ₹{income} | Total Expense: ₹{expense}")

        except Exception as e:
            raise DatabaseConnectionException(f"❌ Error generating financial summary: {e}")

    def tax_employee_join_report(self):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            query = """
            SELECT e.employee_id, e.first_name, e.join_date, t.tax_year, t.taxable_income, t.tax_amount
            FROM employee e
            JOIN tax t ON e.employee_id = t.employee_id
            ORDER BY e.employee_id, t.tax_year
            """
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()
            conn.close()

            print("\n📊 Employee Tax Join Report:")
            for row in rows:
                print(f"Employee ID: {row[0]}, Name: {row[1]}, Join Date: {row[2]}, Year: {row[3]}, Income: ₹{row[4]}, Tax: ₹{row[5]}")
        except Exception as e:
            raise DatabaseConnectionException(f"❌ Error generating tax join report: {e}")

    def high_salary_employees(self, limit):
        try:
            if not isinstance(limit, (int, float)) or limit < 0:
                raise InvalidInputException("Salary limit must be a non-negative number.")

            conn = get_connection()
            cursor = conn.cursor()
            query = """
            SELECT employee_id, basic_salary, net_salary
            FROM payroll
            WHERE net_salary > %s
            """
            cursor.execute(query, (limit,))
            rows = cursor.fetchall()
            cursor.close()
            conn.close()

            print(f"\n📊 Employees with Net Salary > ₹{limit}:")
            for row in rows:
                print(f"Employee ID: {row[0]}, Basic Salary: ₹{row[1]}, Net Salary: ₹{row[2]}")
        except InvalidInputException as e:
            raise e
        except Exception as e:
            raise DatabaseConnectionException(f"❌ Error fetching high salary employees: {e}")
