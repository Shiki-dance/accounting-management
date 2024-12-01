from django import forms
from .models import Expense
from .models import ExpenseCategory

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields =  ['age', 'name', 'amount', 'department',  'institution', 'content', 'date']  
        labels = {
            'age': '代',
            'name': 'ダンサーネーム',
            'amount': '金額',
            'department': '係り',
            'institution' :'借りた施設（渉外のみ）',
            'content': '使った内容',
            'date': '日付',
        }



class ExpenseCategoryForm(forms.ModelForm):
    class Meta:
        model = ExpenseCategory
        fields = ['age', 'name', 'amount', 'category_name', 'date']
        labels = {
            'age': '代',
            'name': 'ダンサーネーム',
            'amount': '金額',
            'category_name': '項目',
            'date': '日付',
        }