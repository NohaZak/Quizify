# Generated by Django 5.1.4 on 2025-01-01 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0006_remove_userprofile_photo_userprofile_profile_picture_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='bio',
            field=models.TextField(blank=True, help_text='Write something about yourself.', null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='preferred_language',
            field=models.CharField(blank=True, help_text='Your preferred language for communication.', max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='timezone',
            field=models.CharField(blank=True, help_text='Your preferred timezone.', max_length=50, null=True),
        ),
    ]