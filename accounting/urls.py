from django.urls import path
from . import views

# accounting/views.py

from django.http import HttpResponse

def index(request):
    return HttpResponse("Welcome to the Accounting App!")

urlpatterns = [
    path('', views.index, name='index'),  # ルートURLに対するビュー
    path('department-expenses/', views.department_expenses, name='department_expenses'),
    path('age-expenses/', views.age_expenses, name='age_expenses'),
    path('monthly-personal-expenses/', views.monthly_personal_expenses, name='monthly_personal_expenses'),
    path('export-department-expenses-pdf/', views.export_department_expenses_pdf, name='export_department_expenses_pdf'),
]

