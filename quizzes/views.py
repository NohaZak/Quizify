from django.shortcuts import render, get_object_or_404
from .models import Quiz, Question

# View for listing all quizzes
def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quizzes/quiz_list.html', {'quizzes': quizzes})

# View for a specific quiz detail
def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()
    return render(request, 'quizzes/quiz_detail.html', {'quiz': quiz, 'questions': questions})
