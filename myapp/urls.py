from django.urls import path
from .views import DepartmentList, CreateDepartment, EmployeeList, CreateEmployee, UpdateEmployee, DeleteEmployee, DeleteDepartment, UpdateDepartment, EmployeeListOrderedBySalary, LoginView

urlpatterns = [
    path('departments/', DepartmentList.as_view(), name='department-list'),
    path('departments/create/', CreateDepartment.as_view(), name='create-department'),
    path('departments/update/<int:pk>/', UpdateDepartment.as_view(), name='update-department'),
    path('departments/delete/<int:pk>/', DeleteDepartment.as_view(), name='delete-department'),

    path('employees/', EmployeeList.as_view(), name='employee-list'),
    path('employees/create/', CreateEmployee.as_view(), name='create-employee'),
    path('employees/update/<str:employee_name>/', UpdateEmployee.as_view(), name='update-employee'),
    path('employees/delete/<str:employee_name>/', DeleteEmployee.as_view(), name='delete_employee'),
    path('employees/ordered_by_salary/', EmployeeListOrderedBySalary.as_view(), name='employees_ordered_by_salary'),

    path('api/login/', LoginView.as_view(), name='login'),  
]
