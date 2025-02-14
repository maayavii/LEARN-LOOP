from django.db import models
from django.contrib.auth.models import User
import datetime

class Exam(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField(default=datetime.date.today)  # Exam date
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_exams', default=1)
    is_published = models.BooleanField(default=False) 
    def __str__(self):
        return self.title

    def get_total_attendees(self):
        return self.results.count()
    
    def can_take_exam(self, user):
            # Check if user hasn't taken the exam yet and exam is published
        return (
            self.is_published and 
            not Result.objects.filter(exam=self, student=user).exists()
        )


class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()

    def __str__(self):
        return self.text

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)  # Flag for correct answer

    def __str__(self):
        return self.text

class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} - {self.question.text}"

    def is_correct(self):
        return self.selected_answer.is_correct

class Result(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='results')
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.FloatField(default=0.0)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.exam.title} - Score: {self.score}"

    def calculate_score(self):
        # Calculate score based on the user's selected answers
        user_answers = UserAnswer.objects.filter(user=self.student, question__exam=self.exam)
        correct_answers = sum([1 for answer in user_answers if answer.is_correct()])
        total_questions = self.exam.questions.count()
        score = (correct_answers / total_questions) * 100  # Calculate percentage score
        self.score = score
        self.save()
