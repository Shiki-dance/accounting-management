from django.shortcuts import render
from .models import Expense
from .forms import ExpenseCategoryForm
from .models import ExpenseCategory
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.http import HttpResponse
# views.py
from django.shortcuts import render, redirect, get_object_or_404 # ここでredirectをインポート
from .forms import ExpenseForm  # ExpenseFormをインポート
from reportlab.pdfgen import canvas  # 追加
from django.contrib import messages
import logging
from itertools import groupby


logger = logging.getLogger(__name__)

# 1. 係りごとの支出合計と内訳
def department_expenses(request):
    departments = Expense.objects.values('department').distinct()
    department_data = {}
    for dept in departments:
        department = dept['department']
        expenses = Expense.objects.filter(department=department)
        total = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
        #金額の合計を計算
        department_data[department] = {
            'total': total,#合計を表示
            'details': expenses,#支出の内訳を表示
        }
    return render(request, 'accounting/department_expenses.html', {'department_data': department_data})

# 2. フォーム入力ビュー

def create_expenses(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()  # フォームデータを保存
            return redirect('expense_list')  # データ保存後、支出リストページにリダイレクト
    else:
        form = ExpenseForm()  # GETリクエスト時は空のフォームを表示

    return render(request, 'accounting/create_expenses.html', {'form': form})
   
from django.shortcuts import render
from .models import Expense  # Expenseモデルをインポート

# 3 支出リストを表示するための処理
def expense_list(request):
    # Expenseモデルから全ての支出データを取得
    expenses = Expense.objects.all()
    return render(request, 'accounting/expense_list.html', {'expenses': expenses})

# 3.1 データ削除

def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)

    if request.method == "POST":

        #ログ記録
        logger.info(f"User{request.user.username} deleted expense with ID {expense.id}, Name: {expense.name}, Amount: {expense.amount}, Department{expense.department}")
        # 削除処理
        expense.delete()

        # 削除完了メッセージ
        messages.success(request, '支出データが削除されました。')

        # 削除後、支出リストページにリダイレクト
        return redirect('expense_list')
    
    return redirect('expense_list')  # POST以外の場合もリダイレクト


# 4. 各代ごとの支出合計と内訳上と同様に行う
def age_expenses(request):
    ages = Expense.objects.values('age').distinct()
    age_data = {}
    for age_entry in ages:
        age = age_entry['age']
        expenses = Expense.objects.filter(age=age)
        total = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
        age_data[age] = {
            'total': total,
            'details': expenses,
        }
    
    return render(request, 'accounting/age_expenses.html', {'age_data': age_data})

# 5. 一人ひとりの月ごとの支出合計
def monthly_personal_expenses(request):
    names = Expense.objects.values('name').distinct()
    personal_data = {}

    for name_entry in names:
        name = name_entry['name']
        monthly_expenses = ( # 月ごとの支出の合計を表示
            Expense.objects
            .filter(name=name)
            .annotate(month=TruncMonth('date')) #月ごとに集計
            .values('month') #'date'を追加して保持
            .annotate(total=Sum('amount') or 0)
            .order_by('month')
        )
        personal_data[name] = monthly_expenses

    return render(request, 'accounting/monthly_personal_expenses.html', {'personal_data': personal_data})

def index(request):
    
    return render(request, 'accounting/index.html') 

def export_department_expenses_pdf(request):
    # HTTPレスポンスをPDF形式で作成
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="department_expenses.pdf"'

    # PDFのキャンバスを作成
    pdf_canvas = canvas.Canvas(response)

    # タイトル
    pdf_canvas.setFont("Helvetica-Bold", 16)
    pdf_canvas.drawString(100, 800, "係りごとの支出一覧")
    pdf_canvas.setFont("Helvetica", 12)

    # データの取得と表示位置の初期化
    y_position = 750
    departments = Expense.objects.values('department').distinct()

    for dept in departments:
        department = dept['department']
        expenses = Expense.objects.filter(department=department)
        total = expenses.aggregate(Sum('amount'))['amount__sum']

        # 係りごとの合計をPDFに追加
        pdf_canvas.drawString(50, y_position, f"係り: {department} - 合計: {total}円")
        y_position -= 20

        # 各支出の詳細を追加
        for expense in expenses:
            pdf_canvas.drawString(70, y_position, f"- {expense.name}: {expense.amount}円（{expense.date}）")
            y_position -= 15

            # ページいっぱいになったら改ページ
            if y_position < 50:
                pdf_canvas.showPage()
                pdf_canvas.setFont("Helvetica", 12)
                y_position = 750

    # PDFを完成させる
    pdf_canvas.save()
    return response

def month_details(request, year, month):
    year = int(year)  # yearを整数に変換
    month = int(month)  # monthを整数に変換
    expenses = Expense.objects.filter(date__year=year, date__month=month)
    total = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    return render(request, 'accounting/month_details.html', {
        'expenses': expenses, 
        'year': year, 
        'month': month, 
        'total': total
    })

def input_category(request):
    if request.method == 'POST':
        form = ExpenseCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('input_category')  # 成功後リダイレクト
    else:
        form = ExpenseCategoryForm()
    return render(request, 'accounting/input_category.html', {'form': form})



def view_public_performance(request):
    performance_expenses = ExpenseCategory.objects.filter(category_name='公演費').order_by('age', 'name')
    grouped_performance_expenses = groupby(performance_expenses, key=lambda x: x.age)
    grouped_performance_expenses = [(age, list(expenses)) for age, expenses in grouped_performance_expenses]
    return render(request, 'accounting/view_public_performance.html', {'grouped_performance_expenses': grouped_performance_expenses})

def view_monthly_fee(request):
    monthly_fee_expenses = ExpenseCategory.objects.filter(category_name='月会費').order_by('age', 'name')
    grouped_monthly_fee_expenses = groupby(monthly_fee_expenses, key=lambda x: x.age)
    grouped_monthly_fee_expenses = [(age, list(expenses)) for age, expenses in grouped_monthly_fee_expenses]
    return render(request, 'accounting/view_monthly_fee.html', {'grouped_monthly_fee_expenses': grouped_monthly_fee_expenses})

def view_dance_party(request):
    dance_party_expenses = ExpenseCategory.objects.filter(category_name='ダンパ費').order_by('age', 'name')
    grouped_dance_party_expenses = groupby(dance_party_expenses, key=lambda x: x.age)
    grouped_dance_party_expenses = [(age, list(expenses)) for age, expenses in grouped_dance_party_expenses]
    return render(request, 'accounting/view_dance_party.html', {'grouped_dance_party_expenses': grouped_dance_party_expenses})
