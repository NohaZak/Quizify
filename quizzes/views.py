from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Max
from .models import Quiz, Result
from .forms import QuizForm

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
            user = form.save()
            login(request, user)
            return redirect('quiz_list')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')  # Redirect authenticated users to the dashboard

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')  # Redirect after successful login
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})

@login_required
def user_dashboard(request):
    user = request.user
    user_results = Result.objects.filter(user=user.username).order_by('-id')[:5]  # Recent 5 results

    # Calculate user statistics
    total_quizzes = Result.objects.filter(user=user.username).count()
    average_score = Result.objects.filter(user=user.username).aggregate(Avg('score'))['score__avg'] or 0
    highest_score_quiz = Result.objects.filter(user=user.username).order_by('-score').first()

    context = {
        'user': user,
        'user_results': user_results,
        'total_quizzes': total_quizzes,
        'average_score': round(average_score, 2),
        'highest_score_quiz': highest_score_quiz,
    }
    return render(request, 'dashboard.html', context)


def user_logout(request):
    logout(request)
    return redirect('login')

def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quizzes/quiz_list.html', {'quizzes': quizzes})

from django.shortcuts import render, get_object_or_404
from .models import Quiz

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
                user=request.user.username if request.user.is_authenticated else "Anonymous",
                quiz=quiz,
                score=score,
            )

            return redirect('quiz_result', quiz_id=quiz.id)
    else:
        form = QuizForm(questions=questions)

    return render(request, 'quizzes/take_quiz.html', {
        'quiz': quiz,
        'form': form,
    })

    return render(request, 'quizzes/take_quiz.html', {
        'quiz': quiz,
        'form': form,
    })


def quiz_result(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.prefetch_related('choices')

    selected_answers = request.session.get('selected_answers', {})
    score = request.session.get('score', 0)
    total = request.session.get('total', 0)

    # Map selected answers to choice texts
    selected_choices = {}
    for question in questions:
        selected_choice_id = selected_answers.get(str(question.id))  # Ensure we fetch by string key
        if selected_choice_id:
            selected_choice = question.choices.filter(id=int(selected_choice_id)).first()
            selected_choices[question.id] = selected_choice.text if selected_choice else "Invalid Choice"

    context = {
        'quiz': quiz,
        'questions': questions,
        'selected_answers': selected_choices,  # Pass the choice text instead of IDs
        'score': score,
        'total': total,
    }

    return render(request, 'quizzes/quiz_result.html', context)
