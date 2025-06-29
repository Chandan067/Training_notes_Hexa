from dao.employee_service import EmployeeService
from entity.employee import Employee
from datetime import datetime
from exceptions.custom_exceptions import InvalidInputException
from util.input_validator import (
    validate_email,
    validate_numeric,
    validate_float,
    validate_not_empty,
    validate_date,
    validate_alpha_name
)

def main():
    emp_service = EmployeeService()

    while True:
        print("\n--- PayXpert Payroll System ---")
        print("1. Add Employee")
        print("2. View All Employees")
        print("3. Get Employee by ID")
        print("4. Update Employee")
        print("5. Delete Employee")
        print("6. Add Payroll")
        print("7. Update Payroll End Date by Payroll ID")
        print("8. View Payroll by Employee ID")
        print("9. Generate Pay Stub by Employee ID and Date Range")
        print("10. Add Tax Record")
        print("11. View Tax by Employee ID")
        print("12. Add Financial Record")
        print("13. View Financial Records by Employee ID")
        print("14. Generate Payroll Summary Report")
        print("15. Generate Payroll Summary With Salary Filter")
        print("16. Generate Tax Summary Report")
        print("17. Generate Financial Summary Report")
        print("18. Exit")

        choice = input("Enter choice: ").strip()

        try:
            if choice == '1':
                first_name = validate_alpha_name(input("First Name: "), "First Name")
                last_name = validate_alpha_name(input("Last Name: "), "Last Name")
                dob = validate_date(input("DOB (YYYY-MM-DD): "), "DOB")
                gender = validate_not_empty(input("Gender: "), "Gender")
                email = validate_email(input("Email: "))
                phone = validate_numeric(input("Phone: "), "Phone")
                address = validate_not_empty(input("Address: "), "Address")
                position = validate_not_empty(input("Position: "), "Position")
                joining_date = validate_date(input("Joining Date (YYYY-MM-DD): "), "Joining Date")

                emp = Employee(None, first_name, last_name, dob, gender, email, phone, address, position, joining_date, None)
                emp_service.add_employee(emp)

            elif choice == '2':
                emp_service.get_all_employees()

            elif choice == '3':
                emp_id = validate_numeric(input("Enter Employee ID: "), "Employee ID")
                emp_service.get_employee_by_id(int(emp_id))

            elif choice == '4':
                emp_id = validate_numeric(input("Enter Employee ID to update: "), "Employee ID")
                updated = Employee(
                    int(emp_id),
                    validate_not_empty(input("First Name: "), "First Name"),
                    validate_not_empty(input("Last Name: "), "Last Name"),
                    validate_date(input("DOB (YYYY-MM-DD): "), "DOB"),
                    validate_not_empty(input("Gender: "), "Gender"),
                    validate_email(input("Email: ")),
                    validate_numeric(input("Phone: "), "Phone"),
                    validate_not_empty(input("Address: "), "Address"),
                    validate_not_empty(input("Position: "), "Position"),
                    validate_date(input("Joining Date (YYYY-MM-DD): "), "Joining Date"),
                    None
                )
                emp_service.update_employee(int(emp_id), updated)

            elif choice == '5':
                emp_id = validate_numeric(input("Enter Employee ID to delete: "), "Employee ID")
                emp_service.delete_employee(int(emp_id))

            elif choice == '6':
                from dao.payroll_service import PayrollService
                from entity.payroll import Payroll
                payroll_service = PayrollService()

                emp_id = int(validate_numeric(input("Enter Employee ID: "), "Employee ID"))
                pay_start = validate_date(input("Enter Pay Start Date (YYYY-MM-DD): "), "Pay Start")
                pay_end_input = input("Enter Pay End Date (YYYY-MM-DD) or leave blank: ").strip()
                pay_end = validate_date(pay_end_input, "Pay End") if pay_end_input else datetime.strptime("2099-12-31", "%Y-%m-%d").date()

                basic_salary = validate_float(input("Enter Basic Salary: "), "Basic Salary")
                deductions = validate_float(input("Enter Deductions: "), "Deductions")
                overtime_hours = int(validate_numeric(input("Enter Overtime Hours: "), "Overtime Hours"))
                overtime_rate = validate_float(input("Enter Overtime Rate: "), "Overtime Rate")
                overtime_pay = overtime_hours * overtime_rate
                net_salary = basic_salary - deductions + overtime_pay

                payroll = Payroll(None, emp_id, pay_start, pay_end, basic_salary, deductions, net_salary, overtime_hours, overtime_rate)
                payroll_service.add_payroll(payroll)

            elif choice == '7':
                from dao.payroll_service import PayrollService
                payroll_service = PayrollService()

                payroll_id = validate_numeric(input("Enter Payroll ID to update: "), "Payroll ID")
                new_end_date = validate_date(input("Enter new Pay End Date (YYYY-MM-DD): "), "New Pay End Date")
                payroll_service.update_payroll(int(payroll_id), new_end_date)

            elif choice == '8':
                from dao.payroll_service import PayrollService
                payroll_service = PayrollService()
                emp_id = validate_numeric(input("Enter Employee ID to view payroll: "), "Employee ID")
                payroll_service.get_payroll_by_employee(int(emp_id))

            elif choice == '9':
                from dao.payroll_service import PayrollService
                emp_id = int(validate_numeric(input("Enter Employee ID: "), "Employee ID"))
                start_date = validate_date(input("Enter Start Date (YYYY-MM-DD): "), "Start Date")
                end_date = validate_date(input("Enter End Date (YYYY-MM-DD): "), "End Date")
                PayrollService().generate_pay_stub_by_period(emp_id, start_date, end_date)

            elif choice == '10':
                from dao.tax_service import TaxService
                from entity.tax import Tax
                tax_service = TaxService()

                emp_id = int(validate_numeric(input("Enter Employee ID: "), "Employee ID"))
                year = int(validate_numeric(input("Enter Tax Year (YYYY): "), "Tax Year"))
                income = validate_float(input("Enter Taxable Income: "), "Taxable Income")
                tax_amount = tax_service.calculate_tax(income)
                tax = Tax(None, emp_id, year, income, tax_amount)
                tax_service.add_tax_record(tax)

            elif choice == '11':
                from dao.tax_service import TaxService
                tax_service = TaxService()
                emp_id = validate_numeric(input("Enter Employee ID to view tax records: "), "Employee ID")
                tax_service.view_tax_by_employee(int(emp_id))

            elif choice == '12':
                from dao.financial_service import FinancialService
                from entity.financial_record import FinancialRecord
                service = FinancialService()

                emp_id = int(validate_numeric(input("Enter Employee ID: "), "Employee ID"))
                date = validate_date(input("Enter Record Date (YYYY-MM-DD): "), "Record Date")
                desc = validate_not_empty(input("Enter Description: "), "Description")
                amount = validate_float(input("Enter Amount: "), "Amount")
                rtype = input("Enter Record Type (income/expense): ").strip().lower()
                if rtype not in ['income', 'expense']:
                    raise InvalidInputException("❌ Record type must be 'income' or 'expense'.")

                record = FinancialRecord(None, emp_id, date, desc, amount, rtype)
                service.add_record(record)

            elif choice == '13':
                from dao.financial_service import FinancialService
                service = FinancialService()
                emp_id = validate_numeric(input("Enter Employee ID to view financial records: "), "Employee ID")
                service.view_records_by_employee(int(emp_id))

            elif choice == '14':
                from dao.report_service import ReportService
                ReportService().payroll_summary()

            elif choice == '15':
                from dao.report_service import ReportService
                threshold = validate_float(input("Enter minimum salary threshold: "), "Salary Threshold")
                ReportService().payroll_summary(threshold)

            elif choice == '16':
                from dao.report_service import ReportService
                ReportService().tax_employee_join_report()

            elif choice == '17':
                from dao.report_service import ReportService
                ReportService().financial_summary()

            elif choice == '18':
                print("Exiting... Goodbye!")
                break

            else:
                print("❌ Invalid choice. Try again.")

        except InvalidInputException as e:
            print(e)
        except Exception as e:
            print(f"❌ Unexpected Error: {e}")

if __name__ == "__main__":
    main()
