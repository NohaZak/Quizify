from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from . import views
from .views import (
    quiz_api_view,
    quiz_list_api_view,
    quiz_search_api_view,
    quiz_by_category_api_view,
    submit_quiz_result_api_view,
)

# Swagger Schema View
schema_view = get_schema_view(
    openapi.Info(
        title="Quizify API",
        default_version='v1',
        description="API documentation for Quizify",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="nohazakaria55@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Main URL Patterns
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

    # API Views
    path('api/quiz/<int:id>/', quiz_api_view, name='quiz_api_view'),
    path('api/quizzes/', quiz_list_api_view, name='quiz_list_api_view'),
    path('api/quizzes/search/', quiz_search_api_view, name='quiz_search_api_view'),
    path('api/quizzes/category/<str:category>/', quiz_by_category_api_view, name='quiz_by_category_api_view'),
    path('api/quizzes/submit_result/', submit_quiz_result_api_view, name='submit_quiz_result_api_view'),

    # Swagger Documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# Serving Media Files in Development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
