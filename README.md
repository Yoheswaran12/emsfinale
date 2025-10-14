<<<<<<< HEAD
# Employee Management System (Django)

This is a minimal, production-ready starter implementing:
- Auth (login/logout)
- Role-based access with Groups (ADMIN / MANAGER / EMPLOYEE)
- Departments & Positions CRUD (Admin)
- Employee CRUD (Admin & Manager)
- Attendance (Admin & Manager mark, employees view own)
- Leave requests (Employees apply; Admin/Manager approve/reject)
- Simple dashboards

## Setup

1. Create venv & install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Migrate & create superuser:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py init_roles
   ```

3. Run server:
   ```bash
   python manage.py runserver
   ```

4. Login as superuser. From Django admin, add yourself to the **ADMIN** group if desired.
   - Create Departments and Positions first
   - Add Employees from **Employees → Add Employee**
   - Managers should be added to the **MANAGER** group
   - Regular staff should be in the **EMPLOYEE** group (added automatically on create)

## Notes
- Media uploads (profile photos) are saved under `media/` (served in development).
- Time zone is set to Asia/Kolkata.
=======
# emsfinale
>>>>>>> d08032ca090e033ed4ab742efbe149692fcedadc
