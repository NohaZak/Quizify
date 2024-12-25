from django.urls import path
from . import views

urlpatterns = [
    path('', views.quiz_list, name='quiz_list'),  # Map root URL to quiz_list view
    path('<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),  # Map detail view for a specific quiz
]
