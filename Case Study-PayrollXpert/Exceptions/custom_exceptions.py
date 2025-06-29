class EmployeeNotFoundException(Exception):
    def __init__(self, emp_id):
        super().__init__(f"❌ Employee with ID {emp_id} not found.")

class TaxRecordNotFoundException(Exception):
    def __init__(self, emp_id):
        super().__init__(f"❌ No tax record found for Employee ID {emp_id}.")

class PayrollNotFoundException(Exception):
    def __init__(self, emp_id):
        super().__init__(f"❌ No payroll record found for Employee ID {emp_id}.")

class PayrollGenerationException(Exception):
    def __init__(self, message="❌ Error generating payroll."):
        super().__init__(message)

class FinancialRecordException(Exception):
    def __init__(self, message="❌ Error in financial record."):
        super().__init__(message)

class InvalidInputException(Exception):
    def __init__(self, message="❌ Invalid input provided."):
        super().__init__(message)

class DatabaseConnectionException(Exception):
    def __init__(self, message="❌ Database connection error."):
        super().__init__(message)

class TaxCalculationException(Exception):
    def __init__(self, message="❌ Error calculating tax."):
        super().__init__(message)
