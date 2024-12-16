from django.contrib import admin
from .models import Expense
from .models import Member, PaymentItem
# Register your models here.

class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('age', 'name', 'amount', 'content', 'date')

admin.site.register(Expense, ExpenseAdmin)

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'generation', 'status')
    list_filter = ('generation', 'status')
    search_fields = ('name',)  # 名前での検索機能を追加

@admin.register(PaymentItem)
class PaymentItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount')
    filter_horizontal = ('members',)  # ManyToManyフィールドのUIを改善