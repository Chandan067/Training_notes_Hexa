import unittest
from dao.financial_service import FinancialService
from entity.financial_record import FinancialRecord
from exceptions.custom_exceptions import FinancialRecordException, InvalidInputException
from util.db_conn_util import get_connection 
from datetime import datetime

class TestFinancialService(unittest.TestCase):

    def setUp(self):
        self.service = FinancialService()

        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM employee WHERE employee_id = 1")
        if not cursor.fetchone():
            cursor.execute("""
                INSERT INTO employee (employee_id, first_name, last_name, DoB, gender, email, phno, address, designation, join_date)
                VALUES (1, 'Test', 'User', '1990-01-01', 'Male', 'test@payxpert.com', '1234567890', 'Test Address', 'Tester', '2023-01-01')
            """)
            conn.commit()
        cursor.close()
        conn.close()

        self.valid_record = FinancialRecord(
            record_id=None,
            employee_id=1,
            record_date="2024-05-01",
            description="Test Income",
            amount=1000.0,
            record_type="income"
        )

        self.invalid_record_type = FinancialRecord(
            record_id=None,
            employee_id=1,
            record_date="2024-05-01",
            description="Invalid",
            amount=1000.0,
            record_type="bonus" 
        )

        self.invalid_amount = FinancialRecord(
            record_id=None,
            employee_id=1,
            record_date="2024-05-01",
            description="Invalid Amount",
            amount=-500,  
            record_type="expense"
        )

        self.invalid_date = FinancialRecord(
            record_id=None,
            employee_id=1,
            record_date="2024/05/01",  
            description="Bad Date",
            amount=500.0,
            record_type="expense"
        )

    def test_add_valid_financial_record(self):
        try:
            self.service.add_record(self.valid_record)
            added = True
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            added = False
        self.assertTrue(added, "✅ Valid financial record should be added.")

    def test_add_invalid_record_type(self):
        with self.assertRaises(FinancialRecordException):
            self.service.add_record(self.invalid_record_type)

    def test_add_invalid_amount(self):
        with self.assertRaises(InvalidInputException):
            self.service.add_record(self.invalid_amount)

    def test_add_invalid_date(self):
        with self.assertRaises(InvalidInputException):
            self.service.add_record(self.invalid_date)

    def test_view_records_by_invalid_id(self):
        with self.assertRaises(InvalidInputException):
            self.service.view_records_by_employee("abc") 

if __name__ == '__main__':
    unittest.main()
