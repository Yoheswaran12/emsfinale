from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    # Departments
    path('departments/', views.department_list, name='department_list'),
    path('departments/add/', views.department_create, name='department_create'),
    path('departments/<int:pk>/edit/', views.department_update, name='department_update'),
    path('departments/<int:pk>/delete/', views.department_delete, name='department_delete'),

    # Positions
    path('positions/', views.position_list, name='position_list'),
    path('positions/add/', views.position_create, name='position_create'),
    path('positions/<int:pk>/edit/', views.position_update, name='position_update'),
    path('positions/<int:pk>/delete/', views.position_delete, name='position_delete'),

    # Employees
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/add/', views.employee_create, name='employee_create'),
    path('employees/<int:user_id>/edit/', views.employee_update, name='employee_update'),
    path('employees/<int:user_id>/delete/', views.employee_delete, name='employee_delete'),

    # Attendance
    path('attendance/', views.attendance_list, name='attendance_list'),
    path('attendance/add/', views.attendance_create, name='attendance_create'),
    path('my-attendance/', views.my_attendance, name='my_attendance'),

    # Leaves
    path('leaves/', views.leave_list, name='leave_list'),
    path('leaves/apply/', views.leave_apply, name='leave_apply'),
    path('my-leaves/', views.my_leaves, name='my_leaves'),
    path('leaves/<int:pk>/approve/', views.leave_approve, name='leave_approve'),
    path('leaves/<int:pk>/reject/', views.leave_reject, name='leave_reject'),
    
    #sessions
    path('sessions/', views.session_list, name='session_list'),

]
