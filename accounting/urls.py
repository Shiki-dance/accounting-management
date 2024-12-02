from django.urls import path
from . import views
from django.shortcuts import render


# accounting/views.py

from django.http import HttpResponse

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('', views.index, name='index'),  # ルートURLに対するビュー
    path('create-expenses/', views.create_expenses, name='create_expenses'),
    path('expense-list/', views.expense_list, name='expense_list'),  # expense_listのURLパターン
    path('department-expenses/', views.department_expenses, name='department_expenses'),
    path('age-expenses/', views.age_expenses, name='age_expenses'),
    path('monthly-personal-expenses/', views.monthly_personal_expenses, name='monthly_personal_expenses'),
    path('export-department-expenses-pdf/', views.export_department_expenses_pdf, name='export_department_expenses_pdf'),
    path('month-details/<int:year>/<int:month>/', views.month_details, name='month_details'),
    path('delete-expense/<int:expense_id>/', views.delete_expense, name='delete_expense'),  # 削除用URLパターン
    path('input_category/', views.input_category, name='input_category'),
    path('view_public_performance/', views.view_public_performance, name='view_public_performance'),
    path('view_monthly_fee/', views.view_monthly_fee, name='view_monthly_fee'),
    path('view_dance_party/', views.view_dance_party, name='view_dance_party'),
]

