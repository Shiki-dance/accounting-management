from django import forms
from .models import Expense

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields =  ['age', 'name', 'amount', 'department', 'institution', 'content', 'date']  
        labels = {
            'age': '代',
            'name': 'ダンサーネーム',
            'amount': '金額',
            'department': '係り',
            'institution': '借りた施設（渉外のみ）',
            'content': '使った内容',
            'date': '日付',
        }