from django.db import models
from django.contrib.auth.models import User

class Quiz(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text


class Choice(models.Model):
    question = models.ForeignKey(Question, related_name="choices", on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    class Meta:
        unique_together = ('question', 'text')  # Prevent duplicate choices for the same question

    def __str__(self):
        return self.text

class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to User model
    quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE)  # Link to Quiz model
    score = models.IntegerField()
    date_taken = models.DateTimeField(auto_now_add=True)  # Automatically set when the result is created

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title} - {self.score}"
