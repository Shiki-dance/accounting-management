from django.db import models

class Expense(models.Model):#すべてのもとになるclass
    DEPARTMENTS = [   #　係りをまとめたもの
        ('渉外', '渉外'),
        ('音響', '音響'),
        ('医務', '医務'),
        ('広報', '広報'),
        ('衣装', '衣装'),
        ('会場', '会場'),
        ('対外交渉', '対外交渉'),
        ('映像', '映像'),
        ('美術', '美術'),
        ('その他', 'その他')
    ]
    # 入力項目
    age = models.IntegerField()
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    department = models.CharField(max_length=10, choices=DEPARTMENTS)
    institution = models.CharField(max_length=100, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    date = models.DateField()

    def __str__(self):
        return f"{self.name} - {self.department} - {self.amount}円"

from django.db import models

# 新しいフォームに対して使用するモデル
class ExpenseCategory(models.Model):
    CATEGORY_CHOICES = (
        ('公演費', '公演費'),
        ('月会費', '月会費'),
        ('ベースメント費', 'ベースメント費'),
    )
    
    age = models.IntegerField()
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category_name = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    date = models.DateField()

    def __str__(self):
        return self.category_name
