
from django.db import models
from django.contrib.auth.models import User

from .models import Word


class WordAnswer(models.Model):
    """
    История ответов пользователя на слова
    """
    word = models.ForeignKey(Word, on_delete=models.CASCADE, related_name='answers')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='word_answers')
    
    is_correct = models.BooleanField()
    answered_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-answered_at']
        indexes = [
            models.Index(fields=['user', 'answered_at']),
            models.Index(fields=['word', 'answered_at']),
        ]
    
    def __str__(self):
        return f"{self.word.word} - {'Correct' if self.is_correct else 'Wrong'} at {self.answered_at}"