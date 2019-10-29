from django.urls import path
from . import views

app_name = 'sudoku_solver_app'
urlpatterns = [
    path('', views.index, name='index'),
]