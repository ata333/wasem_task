import json
from datetime import datetime, date
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Employee, TimeTable, Vacation, Team
from .serializers import EmployeeSerializer, TimeTableSerializer
from django.db.models import Q
from time import mktime


@api_view(['POST'])
def get_token(request):
    valid = False
    try:
        data = list(json.loads(request.body).values())
        userobj = User.objects.get(username=data[0])
        valid = userobj.check_password(data[1])
        result = None
        if (valid):
            try:
                token = Token.objects.get(user=userobj).key
                result = token
            except e:
                result = e
        else:
            result = "The password doesn't match"
    except ObjectDoesNotExist:
        result = "User doesn't exist"
    return Response(result)
        
@api_view(['GET'])
@authentication_classes([TokenAuthentication]) 
@permission_classes((IsAuthenticated,))
def create_team(request, team_name):
    team = Team(name = team_name)
    team.save()
    return Response(team.id)

@api_view(['GET'])
@authentication_classes([TokenAuthentication]) 
@permission_classes((IsAuthenticated,))
def assign_team(request, employee_id, team_id):
    try:
        employee = Employee.objects.get(pk = employee_id)
        team = Team.objects.get(pk = team_id)
        employee.team_id = team
        employee.save()
        result = "Completed"
    except ObjectDoesNotExist:
        result = "Employee or team doesn't exists"
    return Response(result)
    
@api_view(['GET'])
@authentication_classes([TokenAuthentication]) 
@permission_classes((IsAuthenticated,))    
def avg_leave_arrival(request, employee_id):
    try:
        employee = Employee.objects.get(pk = employee_id)
        time_logs = TimeTable.objects.filter(emp_id = employee)
        avg_check_in = 0
        avg_check_out = 0
        number_of_checks = 0
        for time_log in time_logs:
            check_in_time = time_log.check_in_time.strftime('%H:%M').split(":")
            avg_check_in += (int(check_in_time[0]) * 60 * 60 + int(check_in_time[1]) * 60) / 3600
            check_out_time = time_log.check_out_time.strftime('%H:%M').split(":")
            avg_check_out += (int(check_out_time[0]) * 60 * 60 + int(check_out_time[1]) * 60) / 3600
            number_of_checks += 1
        avg_check_in = avg_check_in / number_of_checks
        avg_check_out = avg_check_out / number_of_checks
        avg_check_in_hour = int(avg_check_in)
        avg_check_in_minute = int((avg_check_in * 3600) % 3600 / 60)
        avg_check_out_hour = int(avg_check_out)
        avg_check_out_minute = int((avg_check_out * 3600) % 3600 / 60)
        result = "Average check in: "+ str(avg_check_in_hour) + ":" + str(avg_check_in_minute) + " Average check out: " + str(avg_check_out_hour)+ ":" +str(avg_check_out_minute) 
    except ObjectDoesNotExist:
        result = "Employee doesn't exists"
    return Response(result)
    
    
@api_view(['GET'])
@authentication_classes([TokenAuthentication]) 
@permission_classes((IsAuthenticated,))
def total_working_to_leaving_team(request, team_id):
    team_employees = Employee.objects.filter(team_id = team_id)
    total_seconds = 0
    num_of_leaving_hours = 0
    for employee in team_employees:
        time_logs = TimeTable.objects.filter(emp_id = employee)
        num_of_leaving_hours += Vacation.objects.filter(emp_id = employee, vacation_date__lte = datetime.today()).count() * 8
        for time_log in time_logs:
            total_seconds += (time_log.check_out_time - time_log.check_in_time).total_seconds()
    total_working_hours = total_seconds / 3600
    percentage = total_working_hours / (total_working_hours + num_of_leaving_hours)
    return Response(str(format(percentage,".2f")))
        
         
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes((IsAuthenticated,))   
def get_working_hours(request, employee_id, duration):
    # 0 last week, 1 last quarter, 2 last year
    employee = Employee.objects.get(pk = employee_id)
    my_date = datetime.today()
    from ata_timer.tests import test_config
    TEST = False
    if (hasattr(test_config,"test_get_working_hours_quarter")):
        TEST = test_config.test_get_working_hours_quarter
        if (TEST):
            my_date = datetime(datetime.today().year, 11, 17)
        test_config.test_get_working_hours_quarter = False
    current_year, week_num, day_of_week = my_date.isocalendar()
    if (duration == 0): 
        time_logs = TimeTable.objects.filter(emp_id = employee, current_date__week = week_num)
    elif (duration == 1): 
        current_month = my_date.month
        if (current_month >=1 and current_month <= 3):
            start_date = datetime(current_year, 1, 1)
            end_date = datetime(current_year, 3, 31)
        elif (current_month >=4 and current_month <= 6):
            start_date = datetime(current_year, 4, 1)
            end_date = datetime(current_year, 6, 31)
        elif (current_month >=7 and current_month <= 9):
            start_date = datetime(current_year, 7, 1)
            end_date = datetime(current_year, 9, 31)
        elif (current_month >=10 and current_month <= 12):
            start_date = datetime(current_year, 10, 1)
            end_date = datetime(current_year, 12, 31)
        start_date = datetime.strftime(start_date, '%Y-%m-%d')
        end_date = datetime.strftime(end_date, '%Y-%m-%d')
        time_logs = TimeTable.objects.filter(emp_id = employee, current_date__range=[start_date, end_date])
    else: 
        time_logs = TimeTable.objects.filter(emp_id = employee, current_date__year = current_year)
    total_seconds = 0
    for time_log in time_logs:
        checkout_time = time_log.check_out_time
        if(checkout_time != None):
            total_seconds += (checkout_time - time_log.check_in_time).total_seconds()
        elif(time_log.check_in_time.day < datetime.now().day):
            checkout_time = checkout_time.replace(hour=23, minute=59)
            total_seconds += (checkout_time - time_log.check_in_time).total_seconds()
    total_working_hours = int(total_seconds / 3600)
    minutes_left = int(total_seconds % 3600 / 60)
    return Response(str(total_working_hours) + " hour " + str(minutes_left) + " minute")
    
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes((IsAuthenticated,))
def set_checkout_time(request):
    data = list(json.loads(request.body).values())
    result = "The employee has checked-out"
    try:
        employee = Employee.objects.get(pk = data[1])
        obj = TimeTable.objects.get(emp_id = employee, current_date = datetime.today(), check_out_time = None)
        if (TimeTable.objects.filter(emp_id = employee, current_date = datetime.today(), check_out_time__isnull = False).count() > 0 and not obj):
            result = "The employee has already checked-out"
        else:
            valid = False
            checkout_date_time_obj = datetime.strptime(data[0], '%Y-%m-%d %H:%M:%S')
            if ( checkout_date_time_obj.year == obj.check_in_time.year
            and checkout_date_time_obj.month == obj.check_in_time.month
            and checkout_date_time_obj.day == obj.check_in_time.day): 
                if (checkout_date_time_obj.hour > obj.check_in_time.hour):
                    valid = True
                elif (checkout_date_time_obj.hour == obj.check_in_time.hour):
                    if (checkout_date_time_obj.minute > obj.check_in_time.minute):
                        valid = True
                    elif (checkout_date_time_obj.minute == obj.check_in_time.minute):
                        if (checkout_date_time_obj.second > obj.check_in_time.second or checkout_date_time_obj.second == obj.check_in_time.second):
                            valid = True
            if (valid):
                if (obj.check_in_time.day == checkout_date_time_obj.day):
                    obj.check_out_time = checkout_date_time_obj
                    obj.save()
                else:
                    result = "Invalid check-out"
            else:
                result = "Invalid check-out"
    except ObjectDoesNotExist:
        result = "The employee hasn't checked in"
    return Response(result)

@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes((IsAuthenticated,))
def set_checkin_time(request, employee_id):
    result = "The employee has already checked in"
    employee = Employee.objects.get(pk = employee_id)
    try:
        # if there is some entry with empty checkout don't check in, because you're already checked in
        if (TimeTable.objects.filter(emp_id = employee, current_date = datetime.today()).count() > 0):
            pass
        else:
            raise ObjectDoesNotExist
        if (TimeTable.objects.filter(check_out_time__isnull=True).count() == 0):
            timelog = TimeTable(emp_id = employee)
            timelog.save()
            result = "The employee has checked-in"
        
    except ObjectDoesNotExist:
        timelog = TimeTable(emp_id = employee)
        timelog.save()
        result = "The employee has checked-in"
    return Response(result)


@api_view(['POST'])
@authentication_classes([TokenAuthentication]) 
@permission_classes((IsAuthenticated,))
def take_vacation(request):
    data = list(json.loads(request.body).values())
    try:
        employee = Employee.objects.get(pk = data[1])
    except ObjectDoesNotExist:
        return Response("The employee id doesn't exist")
    try:
        Vacation.objects.get(emp_id = employee, vacation_date = data[0])
        return Response("The employee has already taken a vacation on this date")
    except:
        result = "A vacation has been taken"
        vacation_year = datetime.strptime(data[0], '%Y-%m-%d').year
        now = datetime.now()
        year_now = now.year
        num_of_vacations = Vacation.objects.filter(emp_id = employee).count()
        if (num_of_vacations == 14):
            result = "You can't take a vacation because you have already taken all of your vacations"
        else:
            if (vacation_year == year_now):
                vacation = Vacation(emp_id = employee, vacation_date = data[0])
                vacation.save()
            else:
                result = "Invalid vacation date"
        return Response(result)
    
@api_view(['GET'])
@authentication_classes([TokenAuthentication]) 
@permission_classes((IsAuthenticated,))
def get_employees(request):
    employees = Employee.objects.all()
    serializer = EmployeeSerializer(employees, many=True)
    return Response(serializer.data)
   
@api_view(['GET'])
@authentication_classes([TokenAuthentication]) 
@permission_classes((IsAuthenticated,))
def show_timetable(request):
    timetable = TimeTable.objects.all()
    serializer = TimeTableSerializer(timetable, many=True)
    return Response(serializer.data)
    
@api_view(['GET'])
@authentication_classes([TokenAuthentication]) 
@permission_classes((IsAuthenticated,))
def create_employee(request, employee_name, team_id):
    try:
        employee = Employee(name = employee_name, team_id = Team.objects.get(pk = team_id))
        employee.save()
        result = employee.id
    except ObjectDoesNotExist:
        result = "Team doesn't exist"
    return Response(result)
"""
@api_view(['GET', 'POST'])    
def taskList(request):
    tasks = Task.objects.all()
    # remove the many, get
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)

@api_view(['POST'])      
def create_task(request):
    serializer = TaskSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
    
    return Response(serializer.data)
"""
