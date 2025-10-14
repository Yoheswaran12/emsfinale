from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .decorators import group_required
from .forms import (
    DepartmentForm, PositionForm,
    EmployeeCreateForm, EmployeeUpdateForm,
    AttendanceForm, LeaveForm
)
from .models import Department, Position, EmployeeProfile, Attendance, Leave

from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

@login_required
def dashboard(request):
    # Simple role-aware dashboard
    total_employees = User.objects.filter(is_staff=False).count()
    total_departments = Department.objects.count()
    pending_leaves = Leave.objects.filter(status='PENDING').count()

    my_attendance_count = Attendance.objects.filter(employee=request.user).count()
    my_pending_leaves = Leave.objects.filter(employee=request.user, status='PENDING').count()

    # If manager, show their department stats
    my_dept = getattr(getattr(request.user, 'profile', None), 'department', None)
    dept_employees = User.objects.filter(profile__department=my_dept).count() if my_dept else 0

    return render(request, 'dashboard.html', {
        'total_employees': total_employees,
        'total_departments': total_departments,
        'pending_leaves': pending_leaves,
        'my_attendance_count': my_attendance_count,
        'my_pending_leaves': my_pending_leaves,
        'dept_employees': dept_employees,
        'my_dept': my_dept,
    })

# --- Departments ---
@login_required
@group_required('ADMIN')
def department_list(request):
    items = Department.objects.all()
    return render(request, 'department_list.html', {'items': items})

@login_required
@group_required('ADMIN')
def department_create(request):
    form = DepartmentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Department created.')
        return redirect('department_list')
    return render(request, 'department_form.html', {'form': form})

@login_required
@group_required('ADMIN')
def department_update(request, pk):
    obj = get_object_or_404(Department, pk=pk)
    form = DepartmentForm(request.POST or None, instance=obj)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Department updated.')
        return redirect('department_list')
    return render(request, 'department_form.html', {'form': form})

@login_required
@group_required('ADMIN')
def department_delete(request, pk):
    obj = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Department deleted.')
        return redirect('department_list')
    return render(request, 'confirm_delete.html', {'object': obj, 'title': 'Delete Department'})

# --- Positions ---
@login_required
@group_required('ADMIN')
def position_list(request):
    items = Position.objects.select_related('department').all()
    return render(request, 'position_list.html', {'items': items})

@login_required
@group_required('ADMIN')
def position_create(request):
    form = PositionForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Position created.')
        return redirect('position_list')
    return render(request, 'position_form.html', {'form': form})

@login_required
@group_required('ADMIN')
def position_update(request, pk):
    obj = get_object_or_404(Position, pk=pk)
    form = PositionForm(request.POST or None, instance=obj)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Position updated.')
        return redirect('position_list')
    return render(request, 'position_form.html', {'form': form})

@login_required
@group_required('ADMIN')
def position_delete(request, pk):
    obj = get_object_or_404(Position, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Position deleted.')
        return redirect('position_list')
    return render(request, 'confirm_delete.html', {'object': obj, 'title': 'Delete Position'})

# --- Employees ---
@login_required
@group_required('ADMIN', 'MANAGER')
def employee_list(request):
    q = request.GET.get('q', '').strip()
    users = User.objects.filter(is_superuser=False)
    if q:
        users = users.filter(
            Q(username__icontains=q) |
            Q(first_name__icontains=q) |
            Q(last_name__icontains=q) |
            Q(email__icontains=q)
        )
    # If manager, limit to their department
    if not request.user.is_superuser and request.user.groups.filter(name='MANAGER').exists():
        my_dept = getattr(getattr(request.user, 'profile', None), 'department', None)
        if my_dept:
            users = users.filter(profile__department=my_dept)
    users = users.select_related('profile').order_by('first_name', 'last_name', 'username')
    return render(request, 'employee_list.html', {'users': users, 'q': q})

@login_required
@group_required('ADMIN', 'MANAGER')
def employee_create(request):
    form = EmployeeCreateForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        # default new employee goes to EMPLOYEE group
        employee_group, _ = Group.objects.get_or_create(name='EMPLOYEE')
        user.groups.add(employee_group)
        messages.success(request, 'Employee created.')
        return redirect('employee_list')
    return render(request, 'employee_form.html', {'form': form, 'title': 'Add Employee'})

@login_required
@group_required('ADMIN', 'MANAGER')
def employee_update(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    profile = getattr(user, 'profile', None)
    if profile is None:
        profile = EmployeeProfile.objects.create(user=user)
    if request.method == 'POST':
        form = EmployeeUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            profile.department_id = request.POST.get('department') or None
            profile.position_id = request.POST.get('position') or None
            profile.phone = request.POST.get('phone', '')
            if request.FILES.get('photo'):
                profile.photo = request.FILES['photo']
            profile.save()
            messages.success(request, 'Employee updated.')
            return redirect('employee_list')
    else:
        initial = {
            'department': profile.department_id,
            'position': profile.position_id,
            'phone': profile.phone,
        }
        form = EmployeeUpdateForm(instance=user, initial=initial)
    return render(request, 'employee_form.html', {
    'form': form,
    'user_obj': user,
    'profile': profile,
    'departments': Department.objects.all(),
    'positions': Position.objects.all(),
    'title': 'Edit Employee'
})

@login_required
@group_required('ADMIN', 'MANAGER')
def employee_delete(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'Employee deleted.')
        return redirect('employee_list')
    return render(request, 'confirm_delete.html', {'object': user, 'title': 'Delete Employee'})

# --- Attendance ---
@login_required
@group_required('ADMIN', 'MANAGER')
def attendance_list(request):
    q = request.GET.get('q', '').strip()
    qs = Attendance.objects.select_related('employee', 'employee__profile').all()
    if q:
        qs = qs.filter(Q(employee__username__icontains=q) | Q(employee__first_name__icontains=q) | Q(employee__last_name__icontains=q))
    # Manager sees only their department
    if not request.user.is_superuser and request.user.groups.filter(name='MANAGER').exists():
        my_dept = getattr(getattr(request.user, 'profile', None), 'department', None)
        if my_dept:
            qs = qs.filter(employee__profile__department=my_dept)
    return render(request, 'attendance_list.html', {'items': qs, 'q': q})

@login_required
@group_required('ADMIN', 'MANAGER')
def attendance_create(request):
    form = AttendanceForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        att = form.save(commit=False)
        att.created_by = request.user
        att.save()
        messages.success(request, 'Attendance marked.')
        return redirect('attendance_list')
    return render(request, 'attendance_form.html', {'form': form})

@login_required
def my_attendance(request):
    items = Attendance.objects.filter(employee=request.user).order_by('-date')
    return render(request, 'attendance_list.html', {'items': items, 'my_view': True})

# --- Leaves ---
@login_required
def leave_apply(request):
    form = LeaveForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        leave = form.save(commit=False)
        leave.employee = request.user
        leave.save()
        messages.success(request, 'Leave request submitted.')
        return redirect('my_leaves')
    return render(request, 'leave_form.html', {'form': form})

@login_required
def my_leaves(request):
    items = Leave.objects.filter(employee=request.user).order_by('-applied_at')
    return render(request, 'leave_list.html', {'items': items, 'my_view': True})

@login_required
@group_required('ADMIN', 'MANAGER')
def leave_list(request):
    # Managers see their dept; admins see all
    qs = Leave.objects.select_related('employee', 'employee__profile').all()
    if not request.user.is_superuser and request.user.groups.filter(name='MANAGER').exists():
        my_dept = getattr(getattr(request.user, 'profile', None), 'department', None)
        if my_dept:
            qs = qs.filter(employee__profile__department=my_dept)
    return render(request, 'leave_list.html', {'items': qs})

@login_required
@group_required('ADMIN', 'MANAGER')
def leave_approve(request, pk):
    obj = get_object_or_404(Leave, pk=pk)
    obj.status = 'APPROVED'
    obj.decided_by = request.user
    obj.decided_at = timezone.now()
    obj.save()
    messages.success(request, 'Leave approved.')
    return redirect('leave_list')

@login_required
@group_required('ADMIN', 'MANAGER')
def leave_reject(request, pk):
    obj = get_object_or_404(Leave, pk=pk)
    obj.status = 'REJECTED'
    obj.decided_by = request.user
    obj.decided_at = timezone.now()
    obj.save()
    messages.success(request, 'Leave rejected.')
    return redirect('leave_list')


class RoleBasedLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        user = self.request.user

        if user.is_superuser or user.groups.filter(name='ADMIN').exists():
            return reverse_lazy('dashboard')   # full access dashboard

        elif user.groups.filter(name='MANAGER').exists():
            return reverse_lazy('employee_list')  # e.g. go to employees page

        elif user.groups.filter(name='EMPLOYEE').exists():
            return reverse_lazy('my_attendance')  # e.g. go to their own attendance

        # fallback
        return reverse_lazy('dashboard')
    
from .models import UserSession

@login_required
@group_required('ADMIN', 'MANAGER')
def session_list(request):
    sessions = UserSession.objects.select_related('user').order_by('-login_time')
    return render(request, 'session_list.html', {'sessions': sessions})
