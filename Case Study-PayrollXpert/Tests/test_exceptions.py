import sys
import os


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(r"C:/Users/vvish/Downloads/PayXpertProject3"), '..')))


from exceptions.custom_exceptions import EmployeeNotFoundException, TaxRecordNotFoundException

import unittest
from exceptions.custom_exceptions import EmployeeNotFoundException, TaxRecordNotFoundException

class TestExceptions(unittest.TestCase):
    def test_employee_not_found_exception(self):
        with self.assertRaises(EmployeeNotFoundException):
            raise EmployeeNotFoundException(123)

    def test_tax_record_not_found_exception(self):
        with self.assertRaises(TaxRecordNotFoundException):
            raise TaxRecordNotFoundException(101)

if __name__ == '__main__':
    unittest.main()

