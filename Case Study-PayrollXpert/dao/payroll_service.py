from util.db_conn_util import get_connection
from entity.payroll import Payroll
from exceptions.custom_exceptions import (
    PayrollNotFoundException,
    PayrollGenerationException,
    DatabaseConnectionException,
    InvalidInputException
)


class PayrollService:
    def add_payroll(self, payroll: Payroll):
        conn = None
        cursor = None
        try:
            
            if not isinstance(payroll.basic_salary, (int, float)) or payroll.basic_salary < 0:
                raise InvalidInputException("Basic salary must be a non-negative number.")
            if not isinstance(payroll.deductions, (int, float)) or payroll.deductions < 0:
                raise InvalidInputException("Deductions must be a non-negative number.")
            if not isinstance(payroll.overtime_hours, int) or payroll.overtime_hours < 0:
                raise InvalidInputException("Overtime hours must be a non-negative integer.")
            if not isinstance(payroll.overtime_rate, (int, float)) or payroll.overtime_rate < 0:
                raise InvalidInputException("Overtime rate must be a non-negative number.")

            conn = get_connection()
            cursor = conn.cursor()
            query = """
            INSERT INTO payroll (employee_id, pay_start, pay_end, basic_salary, deductions, net_salary, overtime_hours, overtime_rate)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """

            pay_end = payroll.pay_end if payroll.pay_end not in ("", None) else None

            data = (
                payroll.employee_id,
                payroll.pay_start,
                pay_end,
                payroll.basic_salary,
                payroll.deductions,
                payroll.net_salary,
                payroll.overtime_hours,
                payroll.overtime_rate
            )

            cursor.execute(query, data)
            conn.commit()
            print("✅ Payroll record added successfully.")
        except (PayrollGenerationException, InvalidInputException) as e:
            print(f"❌ Payroll input error: {e}")
        except Exception as e:
            raise DatabaseConnectionException(f"❌ Failed to add payroll record: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_payroll_by_employee(self, emp_id):
        conn = None
        cursor = None
        try:
            if not isinstance(emp_id, int) or emp_id <= 0:
                raise InvalidInputException("Employee ID must be a positive integer.")

            conn = get_connection()
            cursor = conn.cursor()
            query = "SELECT * FROM payroll WHERE employee_id = %s"
            cursor.execute(query, (emp_id,))
            rows = cursor.fetchall()

            if not rows:
                raise PayrollNotFoundException(emp_id)

            print(f"\n📋 Payroll Records for Employee ID {emp_id}:")
            for row in rows:
                pay_end = row[3] if row[3] else "N/A"
                overtime_hours = row[7] or 0
                overtime_rate = row[8] or 0
                overtime_pay = overtime_hours * overtime_rate
                print(f"Payroll ID: {row[0]}, Period: {row[2]} to {pay_end}")
                print(f"Basic: ₹{row[4]}, Deductions: ₹{row[5]}")
                print(f"Overtime: {overtime_hours} hrs * ₹{overtime_rate} = ₹{overtime_pay}")
                print(f"Net Salary: ₹{row[6]}\n")
        except (PayrollNotFoundException, InvalidInputException) as e:
            print(f"❌ {e}")
        except Exception as e:
            raise DatabaseConnectionException(f"❌ Failed to fetch payroll: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def update_payroll(self, payroll_id, updated_pay_end):
        conn = None
        cursor = None
        try:
            
            if not isinstance(payroll_id, int) or payroll_id <= 0:
                raise InvalidInputException("❌ Payroll ID must be a positive integer.")

            conn = get_connection()
            cursor = conn.cursor()

            
            query = "UPDATE payroll SET pay_end = %s WHERE payroll_id = %s"
            cursor.execute(query, (updated_pay_end, payroll_id))
            conn.commit()

            
            if cursor.rowcount == 0:
                raise PayrollNotFoundException(f"❌ Payroll ID {payroll_id} not found.")

            print(f"✅ Payroll ID {payroll_id} updated with new end date: {updated_pay_end}")

        except InvalidInputException as e:
            print(e)
        except PayrollNotFoundException as e:
            print(e)
        except Exception as e:
            raise DatabaseConnectionException(f"❌ Failed to update payroll: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def generate_pay_stub_by_period(self, emp_id, start_date, end_date):
        conn = None
        cursor = None
        try:
            if not isinstance(emp_id, int) or emp_id <= 0:
                raise InvalidInputException("Employee ID must be a positive integer.")

            conn = get_connection()
            cursor = conn.cursor()
            query = """
            SELECT payroll_id, pay_start, pay_end, basic_salary, deductions, net_salary, overtime_hours, overtime_rate
            FROM payroll
            WHERE employee_id = %s AND pay_start >= %s AND (pay_end <= %s OR pay_end IS NULL)
            """
            cursor.execute(query, (emp_id, start_date, end_date))
            rows = cursor.fetchall()

            if not rows:
                raise PayrollNotFoundException(emp_id)

            total_basic = total_deductions = total_overtime = total_net = 0

            print(f"\n🧾 PAY STUB FOR EMPLOYEE ID {emp_id} ({start_date} to {end_date})")
            print("------------------------------------------------------------")

            for row in rows:
                basic, deductions, net, ot_hours, ot_rate = row[3], row[4], row[5], row[6], row[7]
                overtime_pay = ot_hours * ot_rate

                total_basic += basic
                total_deductions += deductions
                total_overtime += overtime_pay
                total_net += net

                print(f"Payroll ID: {row[0]}")
                print(f"  Pay Period: {row[1]} to {row[2]}")
                print(f"  Basic: ₹{basic}, Deductions: ₹{deductions}")
                print(f"  Overtime: {ot_hours} hrs @ ₹{ot_rate} = ₹{overtime_pay}")
                print(f"  Net Salary: ₹{net}")
                print("------------------------------------------------------------")

            print(f"\nTOTALS:")
            print(f"  Basic Salary: ₹{total_basic}")
            print(f"  Deductions: ₹{total_deductions}")
            print(f"  Overtime Pay: ₹{total_overtime}")
            print(f"  Net Salary: ₹{total_net}")
        except (PayrollNotFoundException, InvalidInputException) as e:
            print(f"❌ {e}")
        except Exception as e:
            raise DatabaseConnectionException(f"❌ Failed to generate pay stub: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
