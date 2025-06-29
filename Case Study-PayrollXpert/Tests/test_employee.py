import unittest
from entity.employee import Employee
from datetime import date
from dao.employee_service import EmployeeService
from exceptions.custom_exceptions import EmployeeNotFoundException

class TestEmployeeService(unittest.TestCase):

    def setUp(self):
        self.service = EmployeeService()
        self.sample_employee = Employee(
            None, "Test", "User", date(1995, 5, 15), "Male",
            "test.user@example.com", "1234567890", "Test City",
            "Developer", date(2020, 1, 1), None
        )

    def test_add_employee_success(self):
        try:
            self.service.add_employee(self.sample_employee)
            added = True
        except Exception:
            added = False
        self.assertTrue(added, "Employee should be added without exceptions")

    def test_get_employee_by_invalid_id(self):
        with self.assertRaises(EmployeeNotFoundException):
            self.service.get_employee_by_id(-999)  

    def test_update_non_existing_employee(self):
       
        dummy_emp = Employee(
            -123, "Dummy", "User", date(1990, 1, 1), "Other",
            "dummy@example.com", "0000000000", "Nowhere",
            "Ghost", date(2000, 1, 1), None
        )
        with self.assertRaises(EmployeeNotFoundException):
            self.service.update_employee(-123, dummy_emp)

    def test_delete_invalid_employee(self):
        with self.assertRaises(EmployeeNotFoundException):
            self.service.delete_employee(-404)

if __name__ == '__main__':
    unittest.main()
