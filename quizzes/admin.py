from django.contrib import admin
from .models import Quiz, Question, Choice, Result


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('text', 'question', 'is_correct')  # Display Choice text, associated Question, and correctness
    list_filter = ('question', 'is_correct')  # Allow filtering by Question and correctness
    search_fields = ('text', 'question__text')  # Searchable fields (text and related question text)
    autocomplete_fields = ('question',)  # Autocomplete for Question ForeignKey


class QuestionAdmin(admin.ModelAdmin):
    search_fields = ('text',)  # Make sure Question model is searchable


# Register models
admin.site.register(Quiz)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Result)
