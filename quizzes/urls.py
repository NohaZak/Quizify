from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

# ----------------------------
# Main URL Patterns
# ----------------------------
urlpatterns = [
    # General Views
    path('', views.home_page, name='landing_page'),
    path('home/', views.home_page, name='home_page'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),

    # Admin-Specific Views
    path('admin/', admin.site.urls),
    path('admin-dashboard/', views.admin_user_profile, name='admin_user_profile'),

    # Authentication Views
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.regular_user_profile, name='regular_user_profile'),
    path('dashboard/', views.user_dashboard, name='dashboard'),

    # Quiz Views
    path('quizzes/', views.quiz_list, name='quiz_list'),
    path('quizzes/<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
    path('quizzes/<int:quiz_id>/take/', views.take_quiz, name='take_quiz'),
    path('quizzes/<int:quiz_id>/result/', views.quiz_result, name='quiz_result'),
]

# ----------------------------
# Serving Media Files in Development
# ----------------------------
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
