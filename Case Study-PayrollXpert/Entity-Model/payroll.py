class Payroll:
    def __init__(self, payroll_id, employee_id, pay_start, pay_end,
                 basic_salary, deductions, net_salary,
                 overtime_hours=0, overtime_rate=0):
        self.payroll_id = payroll_id
        self.employee_id = employee_id
        self.pay_start = pay_start
        self.pay_end = pay_end
        self.basic_salary = basic_salary
        self.deductions = deductions
        self.net_salary = net_salary
        self.overtime_hours = overtime_hours
        self.overtime_rate = overtime_rate
