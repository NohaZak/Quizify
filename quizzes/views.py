from django.shortcuts import render, get_object_or_404
from .models import Quiz, Question
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
    questions = quiz.questions.all()

    if request.method == 'POST':
        form = QuizForm(request.POST, questions=questions)
        if form.is_valid():
            score = 0
            for question in questions:
                selected_answer = form.cleaned_data.get(f'question_{question.id}')
                if question.correct_answer and str(question.correct_answer.id) == selected_answer:
                    score += 1

            # Save result
            Result.objects.create(
                user="Anonymous",  # Replace with user object if using authentication
                quiz=quiz,
                score=score,
            )

            return redirect('quiz_detail', quiz_id=quiz.id)

    else:
        form = QuizForm(questions=questions)

    return render(request, 'quizzes/take_quiz.html', {
        'quiz': quiz,
        'form': form,
    })

def quiz_result(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    result = Result.objects.filter(quiz=quiz, user="Anonymous").latest("taken_at")  # Replace "Anonymous" with the logged-in user if authentication is added
    return render(request, "quizzes/quiz_result.html", {"quiz": quiz, "result": result})