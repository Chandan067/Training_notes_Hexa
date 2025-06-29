import unittest
from dao.report_service import ReportService
from exceptions.custom_exceptions import InvalidInputException, DatabaseConnectionException

class TestReportService(unittest.TestCase):

    def setUp(self):
        self.service = ReportService()

    def test_payroll_summary_no_filter(self):
        try:
            self.service.payroll_summary()
        except Exception as e:
            self.fail(f"Unexpected exception raised: {e}")

    def test_payroll_summary_with_valid_filter(self):
        try:
            self.service.payroll_summary(10000.0)
        except Exception as e:
            self.fail(f"Unexpected exception raised: {e}")

    def test_payroll_summary_with_invalid_filter(self):
        with self.assertRaises(InvalidInputException):
            self.service.payroll_summary("invalid")

    def test_high_salary_employees_valid(self):
        try:
            self.service.high_salary_employees(50000.0)
        except Exception as e:
            self.fail(f"Unexpected exception raised: {e}")

    def test_high_salary_employees_invalid(self):
        with self.assertRaises(InvalidInputException):
            self.service.high_salary_employees(-500)

    def test_tax_summary(self):
        try:
            self.service.tax_summary()
        except DatabaseConnectionException:
            self.skipTest("Database connection issue - skipping test.")
        except Exception as e:
            self.fail(f"Unexpected exception raised: {e}")

    def test_financial_summary(self):
        try:
            self.service.financial_summary()
        except DatabaseConnectionException:
            self.skipTest("Database connection issue - skipping test.")
        except Exception as e:
            self.fail(f"Unexpected exception raised: {e}")

    def test_tax_employee_join_report(self):
        try:
            self.service.tax_employee_join_report()
        except DatabaseConnectionException:
            self.skipTest("Database connection issue - skipping test.")
        except Exception as e:
            self.fail(f"Unexpected exception raised: {e}")

if __name__ == "__main__":
    unittest.main()
