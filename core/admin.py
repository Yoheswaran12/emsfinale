from django.contrib import admin
from .models import Department, Position, EmployeeProfile, Attendance, Leave, UserSession

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    search_fields = ['name']

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ['name', 'department']
    list_filter = ['department']
    search_fields = ['name']

@admin.register(EmployeeProfile)
class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'department', 'position', 'phone']
    list_filter = ['department', 'position']
    search_fields = ['user__username', 'user__first_name', 'user__last_name']

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['employee', 'date', 'status', 'created_by']
    list_filter = ['status', 'date']
    search_fields = ['employee__username']

@admin.register(Leave)
class LeaveAdmin(admin.ModelAdmin):
    list_display = ['employee', 'start_date', 'end_date', 'status', 'applied_at', 'decided_by']
    list_filter = ['status', 'start_date', 'end_date']
    search_fields = ['employee__username', 'reason']


@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'login_time', 'logout_time', 'session_duration_human')
    list_filter = ('user', 'login_time', 'logout_time')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')

    def session_duration_human(self, obj):
        return obj.duration_human
    session_duration_human.short_description = "Duration"
