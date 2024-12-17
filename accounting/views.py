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
from .models import Expense
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
import os

logger = logging.getLogger(__name__)

# ログイン設定
from django.contrib.auth import authenticate, login


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # ホームページにリダイレクト
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'accounting/login.html')

from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    # ホームページの処理
    return render(request, 'home.html')


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
    sort_by = request.GET.get('sort_by', 'name')  # URLパラメータで並べ替え基準を取得（デフォルトは'name'）
    ages = Expense.objects.values('age').distinct()
    age_data = {}

    for age_entry in ages:
        age = age_entry['age']
        expenses = Expense.objects.filter(age=age).order_by(sort_by)  # 並べ替え
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

#pdfに出力する
def export_department_expenses_pdf(request):
    # プロジェクトのベースディレクトリを取得
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # フォントファイルへの絶対パスを生成
    font_path = os.path.join(BASE_DIR, 'accounting', 'static', 'accounting', 'css', 'ipaexg.ttf')

    # フォントを登録
    pdfmetrics.registerFont(TTFont('IPAexGothic', font_path))  # IPAexフォントを使用

    # HTTPレスポンスをPDF形式で作成
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="department_expenses.pdf"'

    # PDFのキャンバスを作成
    pdf_canvas = canvas.Canvas(response)

    # タイトル
    pdf_canvas.setFont("IPAexGothic", 16)
    pdf_canvas.drawString(100, 800, "係りごとの支出一覧")
    pdf_canvas.setFont("IPAexGothic", 12)

    y_position = 750
    departments = Expense.objects.values('department').distinct()

    for dept in departments:
        department = dept['department']
        expenses = Expense.objects.filter(department=department)
        total = expenses.aggregate(Sum('amount'))['amount__sum']

        pdf_canvas.drawString(50, y_position, f"係り: {department} - 合計: {total}円")
        y_position -= 20

        for expense in expenses:
            if expense.department == '渉外':
               pdf_canvas.drawString(70, y_position, f"- {expense.name}: {expense.amount}円 {expense.institution}（{expense.date}）")
            else:
               pdf_canvas.drawString(70, y_position, f"- {expense.name}: {expense.amount}円 {expense.content}（{expense.date}）")
            y_position -= 15

            if y_position < 50:
                pdf_canvas.showPage()
                pdf_canvas.setFont("IPAexGothic", 12)
                y_position = 750

    pdf_canvas.save()
    return response


def month_details(request, year, month):
    # 並べ替え基準を取得（デフォルトは 'name'）
    sort_by = request.GET.get('sort_by', 'name')

    # 並べ替え基準が有効でない場合のフォールバック
    if sort_by not in ['name', 'department', 'date']:
        sort_by = 'name'

    # 指定された年と月の支出を取得し、並べ替え
    expenses = Expense.objects.filter(
        date__year=year, date__month=month
    ).order_by(sort_by)

    # 合計金額を計算
    total = expenses.aggregate(Sum('amount'))['amount__sum'] or 0

    # テンプレートにデータを渡す
    return render(request, 'accounting/month_details.html', {
        'year': year,
        'month': month,
        'expenses': expenses,
        'total': total,
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

def category_expense_list(request):
    """ExpenseCategoryのリストを表示するビュー"""
    expenses = ExpenseCategory.objects.all().order_by('-date')  # 日付で並べ替え
    return render(request, 'accounting/category_expense_list.html', {'expenses': expenses})

def delete_category_expense(request, pk):
    """ExpenseCategoryのデータを削除するビュー"""
    expense = get_object_or_404(ExpenseCategory, pk=pk)
    if request.method == 'POST':
        expense.delete()
        messages.success(request, '支出データを削除しました。')
        return redirect('category_expense_list')
    return render(request, 'accounting/delete_confirm.html', {'expense': expense})

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

def view_basement(request):
    basement_expenses = ExpenseCategory.objects.filter(category_name='ダンパ費').order_by('age', 'name')
    grouped_basement_expenses = groupby(basement_expenses, key=lambda x: x.age)
    grouped_basement_expenses = [(age, list(expenses)) for age, expenses in grouped_basement_expenses]
    return render(request, 'accounting/view_basement.html', {'grouped_basement_expenses': grouped_basement_expenses})


from django.shortcuts import render, get_object_or_404
from .models import Member, PaymentItem, PaymentStatus

def member_list(request):
    # 支払い項目一覧を取得
    payment_items = PaymentItem.objects.filter(name__in=['ダンパ費', '夏旅行代', '打ち上げ代'])  
    selected_item = request.GET.get('payment_item')

    # 代ごとの支払いステータスを分類
    categorized_statuses = {}

    if selected_item:
        # 選択された支払い項目を取得
        payment_item = get_object_or_404(PaymentItem, id=selected_item)
        payment_statuses = PaymentStatus.objects.filter(payment_item=payment_item)

        # 支払いステータスを分類
        for status in payment_statuses:
            generation = str(status.member.generation)  # 文字列で統一
            if generation not in categorized_statuses:
                categorized_statuses[generation] = {'paid': [], 'unpaid': []}
            
            # 支払い済みかどうかで分類
            if status.is_paid:
                categorized_statuses[generation]['paid'].append(status)
            else:
                categorized_statuses[generation]['unpaid'].append(status)

    context = {
        'payment_items': payment_items,
        'categorized_statuses': categorized_statuses,
        'selected_item': selected_item,
    }

    return render(request, 'accounting/member_list.html', context)

def tuuzyouki_expenses(request):
    # 支払い項目一覧を取得 (新しい3つの項目のみをフィルタリング)
    payment_items = PaymentItem.objects.filter(name__in=['公演費', '月会費', 'ベースメント費'])  # 例: DEF項目
    selected_item = request.GET.get('payment_item')

    # 代ごとの支払いステータスを分類
    categorized_statuses = {}

    if selected_item:
        # 選択された支払い項目を取得
        payment_item = get_object_or_404(PaymentItem, id=selected_item)
        payment_statuses = PaymentStatus.objects.filter(payment_item=payment_item)

        # 支払いステータスを分類
        for status in payment_statuses:
            generation = str(status.member.generation)  # 文字列で統一
            if generation not in categorized_statuses:
                categorized_statuses[generation] = {'paid': [], 'unpaid': []}
            
            # 支払い済みかどうかで分類
            if status.is_paid:
                categorized_statuses[generation]['paid'].append(status)
            else:
                categorized_statuses[generation]['unpaid'].append(status)

    context = {
        'payment_items': payment_items,
        'categorized_statuses': categorized_statuses,
        'selected_item': selected_item,
    }

    return render(request, 'accounting/tuuzyouki_expenses.html', context)

    

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from .models import PaymentStatus


def update_status_batch(request):
    if request.method == "POST":
        try:
            # POSTデータから必要な情報を取得
            payment_item_id = request.POST.get('payment_item_id')
            checked_member_ids = request.POST.getlist('statuses')  # 空リストになる可能性あり
            redirect_url = request.POST.get('redirect_url', '/accounting/member_list/')

            if not payment_item_id:
                return JsonResponse({'success': False, 'error': 'Invalid data provided'}, status=400)

            # 支払いステータスをリセット (全メンバーの is_paid を False に)
            PaymentStatus.objects.filter(payment_item_id=payment_item_id).update(is_paid=False)

            # チェックされたメンバーのみ支払い済みに更新
            if checked_member_ids:  # checked_member_ids が空でない場合のみ実行
                PaymentStatus.objects.filter(payment_item_id=payment_item_id, member_id__in=checked_member_ids).update(is_paid=True)

            # 動的なリダイレクトURL
            return redirect(f'{redirect_url}?payment_item={payment_item_id}')

        except Exception as e:
            print("Error:", str(e))
            return JsonResponse({'success': False, 'error': 'An error occurred'}, status=500)

    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)

from django.http import JsonResponse
from django.shortcuts import redirect
from .models import PaymentStatus

def reset_status(request):
    if request.method == "POST":
        try:
            payment_item_id = request.POST.get('payment_item_id')

            if not payment_item_id:
                return JsonResponse({'success': False, 'error': 'Invalid data provided'}, status=400)

            # 支払いステータスを全てリセット (is_paid=False)
            PaymentStatus.objects.filter(payment_item_id=payment_item_id).update(is_paid=False)

            return redirect(f'/accounting/member_list/?payment_item={payment_item_id}')
        except Exception as e:
            print("Error:", str(e))
            return JsonResponse({'success': False, 'error': 'An error occurred'}, status=500)

    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
