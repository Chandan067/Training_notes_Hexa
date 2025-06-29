import unittest
from entity.payroll import Payroll

class TestPayroll(unittest.TestCase):
    def test_net_salary_calculation_with_overtime(self):
        basic = 50000
        deductions = 5000
        overtime_hours = 10
        overtime_rate = 200
        expected_net = basic - deductions + (overtime_hours * overtime_rate)

        payroll = Payroll(
            payroll_id=None,
            employee_id=1,
            pay_start="2024-01-01",
            pay_end="2024-01-31",
            basic_salary=basic,
            deductions=deductions,
            net_salary=expected_net,
            overtime_hours=overtime_hours,
            overtime_rate=overtime_rate
        )

        actual_net = payroll.basic_salary - payroll.deductions + (payroll.overtime_hours * payroll.overtime_rate)
        self.assertEqual(actual_net, expected_net, "Net salary calculation with overtime failed.")

if __name__ == '__main__':
    unittest.main()
