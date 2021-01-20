from django.urls import path

from . import views

urlpatterns = [
    path('get_token', views.get_token, name='get_token'),
    path('set_checkin_time/<int:employee_id>', views.set_checkin_time, name='set_checkin_time'),
    path('set_checkout_time', views.set_checkout_time, name='set_checkout_time'),
    path('create_employee/<str:employee_name>/<int:team_id>', views.create_employee, name='create_employee'),
    path('total_working_to_leaving_team/<int:team_id>', views.total_working_to_leaving_team, name='total_working_to_leaving_team'),
    path('create_team/<str:team_name>', views.create_team, name='create_team'),
    path('assign_team/<int:employee_id>/<int:team_id>', views.assign_team, name='assign_team'),
    path('get_employees', views.get_employees, name='get_employees'),
    path('show_timetable', views.show_timetable, name='show_timetable'),
    path('take_vacation', views.take_vacation, name='take_vacation'),
    path('get_working_hours/<int:employee_id>/<int:duration>', views.get_working_hours, name='get_working_hours'),
    path('avg_leave_arrival/<int:employee_id>', views.avg_leave_arrival, name='avg_leave_arrival')
]
