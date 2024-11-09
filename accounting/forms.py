from django import forms
from .models import Expense

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['age', 'name', 'amount', 'department', 'institution', 'content', 'date']
