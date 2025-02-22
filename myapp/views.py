from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from cerberus import Validator
import json
import logging
from django.contrib.auth import authenticate
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Department, Employee, get_session
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.cache import cache  
import logging
logger = logging.getLogger(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)

# Define the department schema
department_schema = {
    "department_name": {
        "type": "string",
        "minlength": 3,
        "maxlength": 100,
        "regex": "^[a-zA-Z ]+$",
        "required": True,
    }
}

employee_schema = {
    "employee_name": {
        "type": "string",
        "minlength": 3,
        "maxlength": 100,
        "regex": "^[a-zA-Z ]+$",
        "required": True,
    },
    "department_name": {
        "type": "string",
        "minlength": 3,
        "maxlength": 100,
        "regex": "^[a-zA-Z ]+$",
        "required": True,
    },
    "employee_salary": {
        "type": "integer",
        "min": 100,
        "required": True,
    },
}

class HomeView(View):
    def get(self, request):
        return JsonResponse({"message": "Welcome to the API!"})

# LoginView
class LoginView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return JsonResponse({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=200)
        else:
            return JsonResponse({"error": "Invalid credentials"}, status=401)

class DepartmentList(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            limit = int(request.GET.get('limit', 10))
            offset = int(request.GET.get('offset', 0))

            if limit <= 0 or offset < 0:
                return JsonResponse({"error": "Invalid limit or offset."}, status=400)
            
            cache_key = f'departments_{limit}_{offset}'
            cached_departments = cache.get(cache_key)
            if cached_departments is not None:
                logger.info("Fetching department data from cache")
                return JsonResponse(cached_departments, safe=False)

            logger.info("Fetching department data from database")
            session = get_session()
            departments = session.query(Department).limit(limit).offset(offset).all()
            department_data = [{"department_id": dept.id, "department_name": dept.department_name} for dept in departments]
            session.close()

            # Cache the result
            cache.set(cache_key, department_data, timeout=3600)  # Cache for 1 hour

            return JsonResponse(department_data, safe=False)
        except Exception as e:
            logger.error(f"Error fetching departments: {e}")
            return JsonResponse({"error": "An error occurred while fetching departments."}, status=500)

class CreateDepartment(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = json.loads(request.body)
        validator = Validator(department_schema)
        if not validator.validate(data):
            return JsonResponse({"error": "Validation error", "details": validator.errors}, status=400)

        try:
            session = get_session()

            existing_department = session.query(Department).filter_by(department_name=data["department_name"]).first()
            if existing_department:
                session.close()
                return JsonResponse({"error": "Department already exists."}, status=400)

            department = Department(department_name=data["department_name"])
            session.add(department)
            session.commit()
            session.close()

            cache.delete_pattern('departments_*') 
            return JsonResponse({"message": "Department created successfully."}, status=201)
        except Exception as e:
            logging.error(f"Error creating department: {e}")
            return JsonResponse({"error": "Failed to create department."}, status=500)

class EmployeeList(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            limit = int(request.GET.get('limit', 10))
            offset = int(request.GET.get('offset', 0))

   
            cache_key = f'employees_{limit}_{offset}'
            cached_employees = cache.get(cache_key)

            if cached_employees is not None:
                logger.info("Fetching employee data from cache.")
                return JsonResponse(cached_employees, safe=False)

            logger.info("Fetching employee data from database.")

            session = get_session()
            employees = session.query(Employee).join(Department).limit(limit).offset(offset).all()

            employee_data = [{"employee_name": emp.name, "department_name": emp.department.department_name, "salary": emp.employee_salary} for emp in employees]
            session.close()


            cache.set(cache_key, employee_data, timeout=3600)  # Cache for 1 hour

            return JsonResponse(employee_data, safe=False)

        except Exception as e:
            logging.error(f"Error fetching employees: {e}")
            return JsonResponse({"error": "An error occurred while fetching employees."}, status=500)


class EmployeeListOrderedBySalary(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            limit = int(request.GET.get('limit', 10))
            offset = int(request.GET.get('offset', 0))

            cache_key = f'employees_salary_{limit}_{offset}'
            cached_employees = cache.get(cache_key)

            if cached_employees is not None:
                logger.info("Fetching employee data (ordered by salary) from cache.")
                return JsonResponse(cached_employees, safe=False)

            logger.info("Fetching employee data (ordered by salary) from database.")

            session = get_session()
            employees = session.query(Employee).join(Department).order_by(Employee.employee_salary.desc()).limit(limit).offset(offset).all()

            employee_data = [{"employee_name": emp.name, "salary": emp.employee_salary, "department_name": emp.department.department_name} for emp in employees]
            session.close()

            cache.set(cache_key, employee_data, timeout=3600)  # Cache for 1 hour

            return JsonResponse(employee_data, safe=False)

        except Exception as e:
            logging.error(f"Error fetching employees by salary: {e}")
            return JsonResponse({"error": "An error occurred while fetching employees."}, status=500)



class CreateEmployee(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = json.loads(request.body)
        validator = Validator(employee_schema)
        if not validator.validate(data):
            return JsonResponse({"error": "Validation error", "details": validator.errors}, status=400)

        try:
            session = get_session()

            department = session.query(Department).filter_by(department_name=data["department_name"]).first()
            if not department:
                department = Department(department_name=data["department_name"])
                session.add(department)
                session.commit()

            employee = Employee(
                name=data["employee_name"],
                department_id=department.id,
                employee_salary=data["employee_salary"]
            )
            session.add(employee)
            session.commit()
            session.close()

            # Clear cached employee lists
            cache.delete_pattern('employees_*')

            return JsonResponse({"message": "Employee created successfully."}, status=201)
        except Exception as e:
            logging.error(f"Error creating employee: {e}")
            return JsonResponse({"error": "Failed to create employee."}, status=500)


class UpdateEmployee(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, employee_name):
        data = json.loads(request.body)
        validator = Validator(employee_schema, require_all=False)
        if not validator.validate(data):
            return JsonResponse({"error": "Validation error", "details": validator.errors}, status=400)

        try:
            session = get_session()

            employee = session.query(Employee).filter_by(name=employee_name).first()
            if not employee:
                return JsonResponse({"error": "Employee not found."}, status=404)

            if "employee_name" in data:
                employee.name = data["employee_name"]
            if "employee_salary" in data:
                employee.employee_salary = data["employee_salary"]
            if "department_name" in data:
                department = session.query(Department).filter_by(department_name=data["department_name"]).first()
                if department:
                    employee.department_id = department.id

            session.commit()
            session.close()


            cache.delete_pattern('employees_*')

            return JsonResponse({"message": "Employee updated successfully."}, status=200)
        except Exception as e:
            logging.error(f"Error updating employee: {e}")
            return JsonResponse({"error": "Failed to update employee."}, status=500)


class DeleteEmployee(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, employee_name):
        try:
            session = get_session()
            employee = session.query(Employee).filter_by(name=employee_name).first()
            if not employee:
                return JsonResponse({"error": "Employee not found."}, status=404)

            session.delete(employee)
            session.commit()
            session.close()

            cache.delete_pattern('employees_*')

            return JsonResponse({"message": "Employee deleted successfully."}, status=200)
        except Exception as e:
            logging.error(f"Error deleting employee: {e}")
            return JsonResponse({"error": "Failed to delete employee."}, status=500)


class DeleteDepartment(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            session = get_session()
            department = session.query(Department).get(pk)
            if not department:
                return JsonResponse({"error": "Department not found."}, status=404)

            session.delete(department)
            session.commit()
            session.close()


            cache.delete_pattern('departments_*')

            return JsonResponse({"message": "Department deleted successfully."}, status=200)
        except Exception as e:
            logging.error(f"Error deleting department: {e}")
            return JsonResponse({"error": "Failed to delete department."}, status=500)


class UpdateDepartment(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            data = json.loads(request.body)

            validator = Validator({
                "department_name": {
                    "type": "string",
                    "regex": "^[a-zA-Z\\s]+$",
                    "minlength": 3,
                    "maxlength": 100,
                    "required": True
                },
            })

            if not validator.validate(data):
                return JsonResponse({"error": "Validation error", "details": validator.errors}, status=400)

            department_name = data.get("department_name")

            session = get_session()
            department = session.query(Department).get(pk)
            if not department:
                session.close()
                return JsonResponse({"error": "Department not found."}, status=404)

            existing_department = session.query(Department).filter_by(department_name=department_name).first()
            if existing_department and existing_department.id != pk:
                session.close()
                return JsonResponse({"error": "Another department with the same name already exists."}, status=400)

            department.department_name = department_name
            session.commit()

            cache.delete_pattern(f"department_{pk}")
            cache.delete_pattern('departments_*')

            session.close()

            return JsonResponse({"message": "Department updated successfully."}, status=200)

        except Exception as e:
            logging.error(f"Error updating department: {e}")
            return JsonResponse({"error": "Failed to update department."}, status=500)
