from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone
from django.db.models import Avg, Count, Max
from .models import Quiz, Result, UserProfile
from urllib.parse import urlparse
from .forms import QuizForm, CustomUserChangeForm, UserProfileForm
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from .serializers import QuizSerializer
from .models import Quiz





# ----------------------------
# General Views
# ----------------------------
def landing_page(request):
    return render(request, 'landing.html')

def home_page(request):
    return render(request, 'home.html')



# ----------------------------
# Authentication Views
# ----------------------------


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = False  # Ensure user is not staff
            user.is_superuser = False  # Ensure user is not admin
            user.save()
            login(request, user)
            messages.success(request, 'Account created successfully! Welcome to Quizify.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the errors below and try again.')
    else:
        form = UserCreationForm()
    
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('/admin/')
        return redirect('regular_user_profile')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'You have successfully logged in.')
            if user.is_superuser:
                return redirect('/admin/')
            return redirect('regular_user_profile')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})


def is_admin(user):
    return user.is_superuser

@login_required
@user_passes_test(is_admin)
def admin_user_profile(request):
    return redirect('/admin/')

# Regular User Profile View
@login_required
def regular_user_profile(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    form = CustomUserChangeForm(request.POST or None, request.FILES or None, instance=request.user)

    if request.method == 'POST' and form.is_valid():
        form.save()
        user_profile.bio = request.POST.get('bio', user_profile.bio)
        user_profile.preferred_language = request.POST.get('preferred_language', user_profile.preferred_language)
        user_profile.timezone = request.POST.get('timezone', user_profile.timezone)
        user_profile.save()
        messages.success(request, 'Your profile was updated successfully!')
        return redirect('regular_user_profile')

    context = {
        'form': form,
        'user_profile': user_profile,
    }
    return render(request, 'profile_regular.html', context)

@login_required
def user_dashboard(request):
    user = request.user
    
    # Fetch user-specific quiz results
    user_results = Result.objects.filter(user=user).order_by('-id')[:5]
    
    # Calculate user statistics
    total_quizzes = Result.objects.filter(user=user).count()
    average_score = Result.objects.filter(user=user).aggregate(Avg('score'))['score__avg'] or 0
    highest_score_quiz = Result.objects.filter(user=user).order_by('-score').first()
    
    # Fetch latest quiz details
    latest_quiz = Result.objects.filter(user=user).order_by('-date_taken').first()
    
    context = {
        'user': user,
        'user_results': user_results,
        'total_quizzes': total_quizzes,
        'average_score': round(average_score, 2),
        'highest_score_quiz': highest_score_quiz,
        'latest_quiz': latest_quiz,
    }
    
    return render(request, 'dashboard.html', context)


def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')

def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quizzes/quiz_list.html', {'quizzes': quizzes})


def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()

    # Fetch previous and next quizzes
    previous_quiz = Quiz.objects.filter(id__lt=quiz_id).order_by('-id').first()
    next_quiz = Quiz.objects.filter(id__gt=quiz_id).order_by('id').first()

    context = {
        'quiz': quiz,
        'questions': questions,
        'previous_quiz': previous_quiz,
        'next_quiz': next_quiz,
    }
    return render(request, 'quizzes/quiz_detail.html', context)


@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.prefetch_related('choices')

    if request.method == 'POST':
        form = QuizForm(request.POST, questions=questions)
        if form.is_valid():
            score = 0
            selected_answers = {}

            for question in questions:
                selected_answer = form.cleaned_data.get(f'question_{question.id}')
                if selected_answer:
                    selected_answers[question.id] = selected_answer
                    correct_choice = question.choices.filter(is_correct=True).first()
                    if correct_choice and str(correct_choice.id) == selected_answer:
                        score += 1

            # Save in session
            request.session['selected_answers'] = selected_answers
            request.session['score'] = score
            request.session['total'] = questions.count()

            # Save result in database
            Result.objects.create(
                user=request.user,
                quiz=quiz,
                score=score,
                date_taken=timezone.now()  # Explicitly set the taken_at timestamp
                )

            return redirect('quiz_result', quiz_id=quiz.id)
    else:
        form = QuizForm(questions=questions)

    return render(request, 'quizzes/take_quiz.html', {
        'quiz': quiz,
        'form': form,
    })

@login_required
def quiz_result(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.prefetch_related('choices')

    selected_answers = request.session.get('selected_answers', {})
    score = request.session.get('score', 0)
    total = request.session.get('total', 0)

    # Map selected answers to choice texts
    selected_choices = {}
    correct_answers = {}

    for question in questions:
        selected_choice_id = selected_answers.get(str(question.id))  # Ensure string key
        selected_choice = question.choices.filter(id=selected_choice_id).first()
        selected_choices[question.id] = selected_choice.text if selected_choice else "No Answer Selected"

        correct_choice = question.choices.filter(is_correct=True).first()
        correct_answers[question.id] = correct_choice.text if correct_choice else "No Correct Answer"

    # Fetch the most recent result for this user and quiz
    result = Result.objects.filter(user=request.user, quiz=quiz).order_by('-date_taken').first()

    # If no result exists, create one
    if not result:
        result = Result.objects.create(
            user=request.user,
            quiz=quiz,
            score=score,
            date_taken=timezone.now()
        )
    else:
        # Update the existing result if necessary
        result.score = score
        result.date_taken = timezone.now()
        result.save()

    context = {
        'quiz': quiz,
        'questions': questions,
        'selected_answers': selected_choices,
        'correct_answers': correct_answers,
        'score': score,
        'total': total,
    }

    return render(request, 'quizzes/quiz_result.html', context)


def leaderboard(request):
    leaderboard_data = (
        Result.objects
        .select_related('user')
        .annotate(
            total_quizzes=Count('id'),
            highest_score=Max('score'),
            average_score=Avg('score')
        )
        .order_by('-highest_score')[:10]
    )

    context = {
        'leaderboard_data': leaderboard_data
    }

    return render(request, 'leaderboard.html', context)

@api_view(['GET'])
@renderer_classes([JSONRenderer])
def quiz_api_view(request, id):
    try:
        quiz = Quiz.objects.get(id=id)
        serializer = QuizSerializer(quiz)
        return Response(serializer.data)
    except Quiz.DoesNotExist:
        return Response({'error': 'Quiz not found'}, status=404)
    
@api_view(['GET'])
def quiz_list_api_view(request):
    from .serializers import QuizSerializer  # Lazy import to avoid circular import
    quizzes = Quiz.objects.all()
    serializer = QuizSerializer(quizzes, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def quiz_search_api_view(request):
    from .serializers import QuizSerializer  # Lazy import to avoid circular import
    query = request.GET.get('q', None)
    if query:
        quizzes = Quiz.objects.filter(title__icontains=query) | Quiz.objects.filter(description__icontains=query)
    else:
        quizzes = Quiz.objects.all()
    serializer = QuizSerializer(quizzes, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def quiz_by_category_api_view(request, category):
    from .serializers import QuizSerializer  # Lazy import to avoid circular import
    quizzes = Quiz.objects.filter(category=category)
    serializer = QuizSerializer(quizzes, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def submit_quiz_result_api_view(request):
    user = request.user
    quiz_id = request.data.get('quiz_id')
    score = request.data.get('score')

    try:
        quiz = Quiz.objects.get(id=quiz_id)
        result = Result.objects.create(user=user, quiz=quiz, score=score, date_taken=timezone.now())
        return Response({'message': 'Result submitted successfully!'}, status=201)
    except Quiz.DoesNotExist:
        return Response({'error': 'Quiz not found'}, status=404)