class Employee:
    def __init__(self, employee_id, first_name, last_name, dob, gender, email,
                 phone, address, position, join_date, termination_date=None):
        self.employee_id = employee_id
        self.first_name = first_name
        self.last_name = last_name
        self.dob = dob
        self.gender = gender
        self.email = email
        self.phone = phone
        self.address = address
        self.position = position
        self.join_date = join_date
        self.termination_date = termination_date