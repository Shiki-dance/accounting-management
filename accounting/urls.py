from django.urls import path
from . import views
from .views import index_view



# accounting/views.py

from django.http import HttpResponse

urlpatterns = [
    path('login/', views.login_view, name='login'), # ログイン登録url
    path('', views.index, name='index'),  # ルートURLに対するビュー
    path("", index_view, name="index"), 
    path('create-expenses/', views.create_expenses, name='create_expenses'), # 係りごとの支出入力フォーム
    path('expense-list/', views.expense_list, name='expense_list'),  # expense_listのURLパターン
    path('department-expenses/', views.department_expenses, name='department_expenses'), #係りごとの支出フォーム
    path('age-expenses/', views.age_expenses, name='age_expenses'), # 代ごとの支出管理ページ
    path('monthly-personal-expenses/', views.monthly_personal_expenses, name='monthly_personal_expenses'), # 月ごとの個人支出
    path('export-department-expenses-pdf/', views.export_department_expenses_pdf, name='export_department_expenses_pdf'),
    path('month-details/<int:year>/<int:month>/', views.month_details, name='month_details'), # 月ごとの詳細ページ
    path('delete-expense/<int:expense_id>/', views.delete_expense, name='delete_expense'),  # 削除用URLパターン
    path('input_category/', views.input_category, name='input_category'), # 通常期入力フォーム
    path('category-expenses/', views.category_expense_list, name='category_expense_list'), # 支出リストのページの作成
    path('delete-category-expense/<int:pk>/', views.delete_category_expense, name='delete_category_expense'),
    path('view_public_performance/', views.view_public_performance, name='view_public_performance'), #公演費
    path('view_monthly_fee/', views.view_monthly_fee, name='view_monthly_fee'), # 月会費
    path('view_basement/', views.view_basement, name='view_basement'), # ベースメント費
    path('update_status_batch/', views.update_status_batch, name='update_status_batch'),
    path('member_list/', views.member_list, name='member_list'),
    path('tuuzyouki_expenses/', views.tuuzyouki_expenses, name='tuuzyouki_expenses'),
    path('reset_status/', views.reset_status, name='reset_status'),
]

