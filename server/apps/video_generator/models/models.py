# models.py
from django.db import models
from django.contrib.auth.models import User

class Word(models.Model):
    """
    English word with translation
    """
    word = models.CharField(max_length=700)
    translation = models.CharField(max_length=700)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='words')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'word']  # Each user can have a word only once
        ordering = ['word']
    
    def __str__(self):
        return f"{self.word} - {self.translation}"

class Text(models.Model):
    """
    Saved text for personal use
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='texts')
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"