"""
URL configuration for accounting_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# accounting_project/urls.py
from django.contrib import admin
from django.urls import include, path
from accounting import views 
# accounting_project/views.py

from django.shortcuts import render

def index(request):
    return render(request, 'index.html')  # 'index.html'を返す

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounting/', include('accounting.urls')),  # accounting.urls をインクルード
    path('', views.index_view, name='index'),  # 追加: ルートURLを処理するビュー
]
