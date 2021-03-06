"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path,include


from bbs import views as bbs_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("bbs.urls")),


    #CAUTION:DRFではURLの冒頭をapiにしなければAPIとして提供されない。出来ればこの指定はconfigのurls.pyに書くべき
    path('api/index/', bbs_views.api_index, name="api_index"),
    path('api/index/<pk>/', bbs_views.api_index, name="api_index"),



]
