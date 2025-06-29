from util.db_conn_util import get_connection
from entity.tax import Tax
from exceptions.custom_exceptions import (
    TaxCalculationException,
    TaxRecordNotFoundException,
    DatabaseConnectionException,
    InvalidInputException
)

class TaxService:
    def calculate_tax(self, income):
        try:
            if not isinstance(income, (int, float)):
                raise InvalidInputException("❌ Income must be a number.")
            if income < 0:
                raise TaxCalculationException("❌ Taxable income must be non-negative.")

            tax = 0
            if income <= 300000:
                tax = 0
            elif income <= 600000:
                tax = (income - 300000) * 0.05
            elif income <= 900000:
                tax = (300000 * 0.05) + (income - 600000) * 0.10
            elif income <= 1200000:
                tax = (300000 * 0.05) + (300000 * 0.10) + (income - 900000) * 0.15
            elif income <= 1500000:
                tax = (300000 * 0.05) + (300000 * 0.10) + (300000 * 0.15) + (income - 1200000) * 0.20
            else:
                tax = (300000 * 0.05) + (300000 * 0.10) + (300000 * 0.15) + (300000 * 0.20) + (income - 1500000) * 0.30

            return round(tax, 2)
        except (TaxCalculationException, InvalidInputException):
            raise
        except Exception as e:
            raise TaxCalculationException(f"❌ Tax calculation error: {e}")

    def add_tax_record(self, tax: Tax):
        conn = None
        cursor = None
        try:
            if not all([
                isinstance(tax.employee_id, int),
                isinstance(tax.tax_year, int),
                isinstance(tax.taxable_income, (int, float)),
                isinstance(tax.tax_amount, (int, float))
            ]):
                raise InvalidInputException("❌ Invalid data types in tax record.")

            if tax.taxable_income < 0:
                raise InvalidInputException("❌ Taxable income must be non-negative.")
            if tax.tax_amount < 0:
                raise InvalidInputException("❌ Tax amount cannot be negative.")
            if tax.tax_year < 1900 or tax.tax_year > 2100:
                raise InvalidInputException("❌ Tax year is out of valid range.")

            conn = get_connection()
            cursor = conn.cursor()
            query = """
            INSERT INTO tax (employee_id, tax_year, taxable_income, tax_amount)
            VALUES (%s, %s, %s, %s)
            """
            data = (tax.employee_id, tax.tax_year, tax.taxable_income, tax.tax_amount)
            cursor.execute(query, data)
            conn.commit()
            print("✅ Tax record added successfully.")
        except InvalidInputException as e:
            print(e)
        except Exception as e:
            raise DatabaseConnectionException(f"❌ Failed to add tax record: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def view_tax_by_employee(self, emp_id):
        conn = None
        cursor = None
        try:
            if not isinstance(emp_id, int):
                raise InvalidInputException("❌ Employee ID must be numeric.")

            conn = get_connection()
            cursor = conn.cursor()
            query = "SELECT * FROM tax WHERE employee_id = %s"
            cursor.execute(query, (emp_id,))
            rows = cursor.fetchall()

            if not rows:
                raise TaxRecordNotFoundException(emp_id)

            print(f"\n📋 Tax Records for Employee ID {emp_id}:")
            for row in rows:
                print(f"Year: {row[2]}, Income: ₹{row[3]}, Tax Paid: ₹{row[4]}")
        except (TaxRecordNotFoundException, InvalidInputException) as e:
            print(e)
        except Exception as e:
            raise DatabaseConnectionException(f"❌ Failed to retrieve tax records: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
