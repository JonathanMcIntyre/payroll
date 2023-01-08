from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('statement/<str:statementId>', views.statement, name='statement'),
    path('employees', views.employees, name='employees'),
    path('paystatements', views.paystatements, name='paystatements'),
    path('paysubmission', views.paysubmission, name='paysubmission')
]
