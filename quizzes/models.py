from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(
        upload_to='profile_photos/',
        default='profile_photos/default.png',
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.user.username}'s Profile"

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)  # Create profile for new user
    else:
        instance.userprofile.save()  # Save profile when user is updated
    
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
