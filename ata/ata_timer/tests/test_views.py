from .test_setup import TestSetup
from ata_timer.models import Employee, TimeTable, Vacation, Team
from datetime import datetime


class TestViews(TestSetup):
    def setUpTestData():
        team = Team(name = "ReactPython")
        team.save()
        employee = Employee(name = "waseem", team_id = team)
        employee.save()
    
    def test_user_can_receive_token(self):
        res = self.client.post(self.get_token_url, self.get_token_body, format="json")
        self.assertEqual(res.data, self.token)
        
    def test_employee_check_in(self):
        res = self.client.get(self.set_checkin_time_url)
        employee = Employee.objects.get(pk = 1)
        count = TimeTable.objects.filter(emp_id = employee, current_date = datetime.today()).count()
        self.assertEqual(count, 1)
    
    def test_employee_check_out_invalid_date(self):
        employee = Employee.objects.get(pk = 1)
        # do a check in
        timelog = TimeTable(emp_id = employee)
        timelog.save()
        res = self.client.post(self.set_checkout_time_url, self.checkout_body_invalid_date, format="json")
        self.assertEqual(res.data, "Invalid check-out")
    
    def test_employee_check_out_valid_date(self):
        employee = Employee.objects.get(pk = 1)
        # do a check in
        timelog = TimeTable(emp_id = employee)
        timelog.save()
        res = self.client.post(self.set_checkout_time_url, self.checkout_body_valid_date, format="json")
        checkout_datetime_obj = datetime.strptime("2021-01-15 18:49:08", '%Y-%m-%d %H:%M:%S')
        count = TimeTable.objects.filter(emp_id = employee, current_date = datetime.today()).count()

    def test_take_vacation(self):
        self.client.post(self.take_vacation_url, self.vacation_body, format="json")
        self.assertNotEqual(Vacation.objects.get(pk = 1), None)
        
    def test_take_vacation_invalid_date(self):
        res = self.client.post(self.take_vacation_url, self.vacation_body_invalid_date, format="json")
        self.assertEqual(res.data, "Invalid vacation date")
        
    def test_take_vacation_all_your_vacations(self):
        employee = Employee.objects.get(pk = 1)
        for i in range(14):
            vacation = Vacation(emp_id = employee, vacation_date = datetime.strptime(self.vacation_body["vacation_date"], '%Y-%m-%d').replace(day=i+1))
            vacation.save()
        res = self.client.post(self.take_vacation_url, self.vacation_body, format="json")
        self.assertEqual(res.data, "You can't take a vacation because you have already taken all of your vacations")
        
    def test_create_employee(self):
        res = self.client.get(self.create_employee_url, **self.header)
        self.assertNotEqual(Employee.objects.get(pk = 2), None)
        
    def test_total_working_to_leaving_team(self):
        employee = Employee.objects.get(pk = 1)
        timelog = TimeTable(emp_id = employee, check_in_time = datetime.now().replace(hour= 1), check_out_time = datetime.now().replace(hour= 7))
        timelog.save()
        res = self.client.get(self.total_working_to_leaving_team_url)
        self.assertEqual(res.data, '1.00')
	
    def test_total_working_to_leaving_team_with_vacation(self):
        employee = Employee.objects.get(pk = 1)
        timelog = TimeTable(emp_id = employee, check_in_time = datetime.now().replace(hour= 1), check_out_time = datetime.now().replace(hour= 9))
        timelog.save()
        vacation = Vacation(emp_id = employee, vacation_date = datetime(2020, 5, 17))
        vacation.save()
        res = self.client.get(self.total_working_to_leaving_team_url)
        self.assertEqual(res.data, '0.50')
        
    def test_create_team(self):
        res = self.client.get(self.create_team_url)
        self.assertNotEqual(Team.objects.get(pk = 2), None)
        
    def test_get_working_hours_week(self):
        employee = Employee.objects.get(pk = 1)
        timelog = TimeTable(emp_id = employee, check_in_time = datetime.now().replace(hour= 1), check_out_time = datetime.now().replace(hour= 9))
        timelog.save()
        res = self.client.get(self.get_working_hours_week_url)
        self.assertEqual(res.data, "8 hour 0 minute")
    
        
    def test_get_working_hours_quarter(self):
        from ata_timer.tests import test_config
        test_config.test_get_working_hours_quarter = True
        employee = Employee.objects.get(pk = 1)
        timelog1 = TimeTable(current_date = datetime(datetime.now().year, 10, 1), emp_id = employee, check_in_time = datetime(datetime.now().year, 11, 1, 12, 00), check_out_time = datetime(datetime.now().year, 11, 1, 18, 00))
        timelog1.save()
        timelog2 = TimeTable(current_date = datetime(datetime.now().year, 10, 1), emp_id = employee, check_in_time = datetime(datetime.now().year, 10, 1, 12, 00), check_out_time = datetime(datetime.now().year, 10, 1, 18, 00))
        timelog2.save()
        res = self.client.get(self.get_working_hours_quarter_url)
        self.assertEqual(res.data, "12 hour 0 minute")
    
    def test_get_working_hours_year(self):
        from ata_timer.tests import test_config
        test_config.test_get_working_hours_quarter = True
        employee = Employee.objects.get(pk = 1)
        timelog1 = TimeTable(current_date = datetime(datetime.now().year, 10, 1), emp_id = employee, check_in_time = datetime(datetime.now().year, 11, 1, 12, 00), check_out_time = datetime(datetime.now().year, 11, 1, 18, 00))
        timelog1.save()
        timelog2 = TimeTable(current_date = datetime(datetime.now().year, 10, 1), emp_id = employee, check_in_time = datetime(datetime.now().year, 10, 1, 12, 00), check_out_time = datetime(datetime.now().year, 10, 1, 18, 00))
        timelog2.save()
        timelog2 = TimeTable(current_date = datetime(datetime.now().year, 1, 1), emp_id = employee, check_in_time = datetime(datetime.now().year, 10, 1, 12, 00), check_out_time = datetime(datetime.now().year, 10, 1, 18, 00))
        timelog2.save()
        res = self.client.get(self.get_working_hours_year_url)
        self.assertEqual(res.data, "18 hour 0 minute")
        
    def test_avg_leave_arrival_url(self):
        employee = Employee.objects.get(pk = 1)
        timelog1 = TimeTable(current_date = datetime(datetime.now().year, 10, 1), emp_id = employee, check_in_time = datetime(datetime.now().year, 11, 1, 12, 35), check_out_time = datetime(datetime.now().year, 11, 1, 18, 10))
        timelog1.save()
        timelog2 = TimeTable(current_date = datetime(datetime.now().year, 10, 1), emp_id = employee, check_in_time = datetime(datetime.now().year, 10, 1, 12, 34), check_out_time = datetime(datetime.now().year, 10, 1, 18, 7))
        timelog2.save()
        timelog2 = TimeTable(current_date = datetime(datetime.now().year, 1, 1), emp_id = employee, check_in_time = datetime(datetime.now().year, 10, 1, 12, 00), check_out_time = datetime(datetime.now().year, 10, 1, 18, 9))
        timelog2.save()
        res = self.client.get(self.avg_leave_arrival_url)
        self.assertEqual(res.data, "Average check in: 12:23 Average check out: 18:8")
        
        

        
