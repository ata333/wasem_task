from django.db import models    
from datetime import datetime    

class Team(models.Model):
    name = models.CharField(max_length=50)
    
    
class Employee(models.Model):
    name = models.CharField(max_length=50)
    team_id = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, db_index=True)
    
    
class TimeTable(models.Model):
    current_date = models.DateField(default=datetime.now, db_index=True)
    check_in_time = models.DateTimeField('check in time', default=datetime.now)
    check_out_time = models.DateTimeField('check out time', null=True)
    emp_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    
class Vacation(models.Model):
    vacation_date = models.DateField("Vacation date")
    emp_id = models.ForeignKey(Employee, on_delete=models.CASCADE, db_index=True)
    


