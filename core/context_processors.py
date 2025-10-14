def role_context(request):
    role = None
    if request.user.is_authenticated:
        if request.user.is_superuser or request.user.groups.filter(name="ADMIN").exists():
            role = "ADMIN"
        elif request.user.groups.filter(name="MANAGER").exists():
            role = "MANAGER"
        elif request.user.groups.filter(name="EMPLOYEE").exists():
            role = "EMPLOYEE"
    return {"role": role}
