from util.db_conn_util import get_connection
from entity.financial_record import FinancialRecord
from exceptions.custom_exceptions import (
    FinancialRecordException,
    DatabaseConnectionException,
    InvalidInputException
)
from util.input_validator import (
    validate_numeric,
    validate_date,
    validate_positive_number,
    validate_not_empty
)

class FinancialService:
    def add_record(self, record: FinancialRecord):
        conn = None
        cursor = None
        try:
            validate_numeric(str(record.employee_id), "Employee ID")
            record.record_date = validate_date(record.record_date, "Record Date")
            record.description = validate_not_empty(record.description, "Description")
            record.amount = validate_positive_number(str(record.amount), "Amount")

            if record.record_type not in ("income", "expense"):
                raise FinancialRecordException("Record type must be either 'income' or 'expense'.")

            conn = get_connection()
            cursor = conn.cursor()
            query = """
            INSERT INTO financial_record (employee_id, record_date, description, amount, record_type)
            VALUES (%s, %s, %s, %s, %s)
            """
            data = (
                record.employee_id,
                record.record_date,
                record.description,
                record.amount,
                record.record_type
            )
            cursor.execute(query, data)
            conn.commit()
            print("✅ Financial record added successfully.")
        except (FinancialRecordException, InvalidInputException) as e:
            print(f"❌ Invalid financial record: {e}")
            raise 
        except Exception as e:
            raise DatabaseConnectionException(f"❌ Failed to add financial record: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def view_records_by_employee(self, emp_id):
        conn = None
        cursor = None
        try:
            emp_id = int(validate_numeric(str(emp_id), "Employee ID"))

            conn = get_connection()
            cursor = conn.cursor()
            query = "SELECT * FROM financial_record WHERE employee_id = %s"
            cursor.execute(query, (emp_id,))
            rows = cursor.fetchall()

            if not rows:
                raise FinancialRecordException(f"No financial records found for Employee ID {emp_id}.")

            print(f"\n📋 Financial Records for Employee ID {emp_id}:")
            for row in rows:
                print(f"{row[2]} | {row[3]} | ₹{row[4]} | {row[5]}")
        except (FinancialRecordException, InvalidInputException) as e:
            print(f"❌ {e}")
            raise 
        except Exception as e:
            raise DatabaseConnectionException(f"❌ Failed to retrieve financial records: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
