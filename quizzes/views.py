from django.shortcuts import render, get_object_or_404, redirect
from .models import Quiz, Result
from .forms import QuizForm

def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quizzes/quiz_list.html', {'quizzes': quizzes})

def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()
    return render(request, 'quizzes/quiz_detail.html', {'quiz': quiz, 'questions': questions})

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


def quiz_result(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.prefetch_related('choices')

    selected_answers = request.session.get('selected_answers', {})
    score = request.session.get('score', 0)
    total = request.session.get('total', 0)

    context = {
        'quiz': quiz,
        'questions': questions,
        'selected_answers': selected_answers,
        'score': score,
        'total': total,
    }

    return render(request, 'quizzes/quiz_result.html', context)
