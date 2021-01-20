from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from datetime import datetime, date
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class TestSetup(APITestCase):
    def setUp(self):
        user = User.objects.create_user(username='ata2', email='ata998@gmail.com', password='ata123123')
        user.save()
        Token.objects.create(user=user)
        self.token = Token.objects.get(user=user).key
        self.header = {'Authorization': 'Token ' + self.token}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        self.get_token_url = reverse("get_token")
        self.set_checkin_time_url = reverse("set_checkin_time", args=[1])
        self.set_checkout_time_url = reverse("set_checkout_time")
        self.create_employee_url = reverse("create_employee", args=["Abu Ali", 1])
        self.total_working_to_leaving_team_url = reverse("total_working_to_leaving_team", args=[1])
        self.create_team_url = reverse("create_team", args=[1])
        self.assign_team_url = reverse("assign_team", args=[1, 1])
        self.get_employees_url = reverse("get_employees")
        self.show_timetable_url = reverse("show_timetable")
        self.take_vacation_url = reverse("take_vacation")
        self.get_working_hours_week_url = reverse("get_working_hours", args=[1, 0])
        self.get_working_hours_quarter_url = reverse("get_working_hours", args=[1, 1])
        self.get_working_hours_year_url = reverse("get_working_hours", args=[1, 2])
        self.avg_leave_arrival_url = reverse("avg_leave_arrival", args=[1])
        self.checkout_body_invalid_date = {
            "checkout_time": "2021-01-15 18:49:08",
            "employee_id": "1"
        }
        self.checkout_body_valid_date = {
            "checkout_time": datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
            "employee_id": "1"
        }
        self.get_token_body = {
        "username" : "ata2",
        "password" : "ata123123"}
        
        self.vacation_body = {
            "vacation_date": "2021-12-19",
            "employee_id": "1"
        }
        self.vacation_body_invalid_date = {
            "vacation_date": "2022-12-19",
            "employee_id": "1"
        }
        return super().setUp()
        
    #def tearDown(self):
        #return super.tearDown()
