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
    
# チェックリストの表示
#メンバーのモデル
class Member(models.Model):
    name = models.CharField(max_length=100)
    generation = models.IntegerField()
    # 支払い済みかどうか（チェックボックスに対応）
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.generation}代 - {self.name}"
# 支払い項目のモデル
class PaymentItem(models.Model):
    name = models.CharField(max_length=100)  # 例: 打ち上げ代
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # デフォルト値を設定
    members = models.ManyToManyField(Member, related_name='payment_items')  # 多対多の関係

    def __str__(self):
        return self.name

# 支払い状況を管理する中間テーブル
class PaymentStatus(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    payment_item = models.ForeignKey(PaymentItem, on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)  # 支払い済みか否か

    class Meta:
        unique_together = ('member', 'payment_item')  # 同じ組み合わせの重複を防ぐ

    def __str__(self):
        return f"{self.member.name} - {self.payment_item.name} - {'支払い済み' if self.is_paid else '未払い'}"



