from django.shortcuts import render
from .models import Expense
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.http import HttpResponse
# views.py
from reportlab.pdfgen import canvas  # 追加


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
            .annotate(month=TruncMonth('date'))
            .values('month')
            .annotate(total=Sum('amount') or 0)
            .order_by('month')
        )
        personal_data[name] = monthly_expenses

    return render(request, 'accounting/monthly_personal_expenses.html', {'personal_data': personal_data})

def index(request):
    
    return render(request, 'index.html') 

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