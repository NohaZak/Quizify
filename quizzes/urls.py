from django.urls import path
from . import views

urlpatterns = [
    # General Views
    path('', views.home_page, name='landing_page'),  # Default landing page
    path('home/', views.home_page, name='home_page'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),


    # Authentication Views
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.user_dashboard, name='dashboard'),


    # Quiz Views
    path('quizzes/', views.quiz_list, name='quiz_list'),  # Changed to 'quizzes/' for clarity
    path('quizzes/<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
    path('quizzes/<int:quiz_id>/take/', views.take_quiz, name='take_quiz'),
    path('quizzes/<int:quiz_id>/result/', views.quiz_result, name='quiz_result'),
]
