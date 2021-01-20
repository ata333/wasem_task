from django.test import TestCase
from ata_timer.models import Employee, TimeTable, Vacation, Team
from rest_framework.test import APITestCase
from datetime import datetime

class TestModels(APITestCase):

    def setUpTestData():
        team = Team(name = "ReactPython")
        team.save()
        employee = Employee(name = "waseem", team_id = team)
        employee.save()
        
    def test_TimeTable(self):
        employee = Employee.objects.get(pk = 1)
        obj = TimeTable(emp_id = employee, check_out_time = None)
        obj.save()
        today_date = datetime.strftime(datetime.today(), '%Y-%m-%d')
        check_in_time = datetime.strftime(obj.check_in_time, '%Y-%m-%d')
        current_date = datetime.strftime(obj.current_date, '%Y-%m-%d')
        self.assertEqual(today_date, check_in_time)
        self.assertEqual(today_date, current_date)
