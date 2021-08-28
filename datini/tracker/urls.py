from django.urls import path

from .views import expenses_list, ExpenseAddView, clan

urlpatterns = [
    path('', expenses_list, name="expenses_list"),
    path('add', ExpenseAddView.as_view(), name="expenses_add"),
    path('clan', clan, name="clan"),
]
