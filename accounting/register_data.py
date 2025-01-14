# スクリプトを実行するには、Django環境をロードする必要があります
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'accounting_project.settings')
django.setup()

from accounting.models import Member, PaymentItem

# PaymentItemを登録
def register_data():
    # PaymentItemを登録
    payment_items = [
    {'name': '打ち上げ代', 'amount': 1000},
    {'name': '夏旅行代', 'amount': 5000},
    {'name': 'ダンパ費', 'amount': 2000},
    {'name': '月会費', 'amount': 2000},
    {'name': '公演費', 'amount': 2000},
    {'name': 'ベースメント費', 'amount': 2000},
]
    for item in payment_items:
        PaymentItem.objects.get_or_create(name=item['name'], defaults={'amount': item['amount']})

# Memberを登録
    members = [
        {'name': '∞', 'generation': 23},
        {'name': 'おんぷ', 'generation': 23},
        {'name': 'カール', 'generation': 23},
        {'name': 'かんちゃん', 'generation': 23},
        {'name': 'koh', 'generation': 23},
        {'name': 'ササ', 'generation': 23},
        {'name': 'シキ', 'generation': 23},
        {'name': 'ジン', 'generation': 23},
        {'name': 'デイジー', 'generation': 23},
        {'name': '那由多', 'generation': 23},
        {'name': 'Nala', 'generation': 23},
        {'name': 'knit', 'generation': 23},
        {'name': 'ねね', 'generation': 23},
        {'name': '破楽', 'generation': 23},
        {'name': 'フェノ', 'generation': 23},
        {'name': 'Bell', 'generation': 23},
        {'name': 'みこと', 'generation': 23},
        {'name': 'みたらし', 'generation': 23},
        {'name': 'ヤマト', 'generation': 23},
        {'name': 'らん', 'generation': 23},
        {'name': 'りん', 'generation': 23},
        {'name': 'るぅ', 'generation': 23},
        {'name': 'Y.K', 'generation': 23},
        {'name': 'WANDA', 'generation': 23},
        {'name': 'A', 'generation': 24},
        {'name': 'est.', 'generation': 24},
        {'name': 'wing_skee', 'generation': 24},
        {'name': 'W', 'generation': 24},
        {'name': '尾崎', 'generation': 24},
        {'name': 'cacao', 'generation': 24},
        {'name': 'Kiko', 'generation': 24},
        {'name': 'ぐく', 'generation': 24},
        {'name': 'saki', 'generation': 24},
        {'name': 'サモ', 'generation': 24},
        {'name': 'しぃら', 'generation': 24},
        {'name': 'ジュニ', 'generation': 24},
        {'name': 'jiro', 'generation': 24},
        {'name': 'ちぇだー', 'generation': 24},
        {'name': 'CHIKI', 'generation': 24},
        {'name': 'chaco', 'generation': 24},
        {'name': 'てぃな', 'generation': 24},
        {'name': 'Ten', 'generation': 24},
        {'name': 'ひなか', 'generation': 24},
        {'name': '舞', 'generation': 24},
        {'name': 'MARIN', 'generation': 24},
        {'name': 'ミオ', 'generation': 24},
        {'name': 'Melia', 'generation': 24},
        {'name': 'mEmma', 'generation': 24},
        {'name': 'モア', 'generation': 24},
        {'name': 'ヨル', 'generation': 24},
        {'name': 'Rara', 'generation': 24},
        {'name': 'れおん', 'generation': 24},
        {'name': 'レン', 'generation': 24},
]

    for member in members:
        Member.objects.get_or_create(name=member['name'], generation=member['generation'])
