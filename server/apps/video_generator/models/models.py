from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=700)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} - {self.description}"

class Word(models.Model):
    """
    English word with translation
    """
    word = models.CharField(max_length=700)
    translation = models.CharField(max_length=700)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='words')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='words', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # example_sentence = models.TextField(blank=True, null=True)
    # example_translation = models.TextField(blank=True, null=True)
    # part_of_speech = models.CharField(max_length=50, blank=True, null=True)  # noun, verb, adjective, etc.
    # pronunciation = models.CharField(max_length=200, blank=True, null=True)  # IPA or audio URL
    # definition = models.TextField(blank=True, null=True)  # Definition in English
    notes = models.TextField(blank=True, null=True)  # Personal notes
    tags = models.CharField(max_length=500, blank=True, null=True)  # Comma-separated tags    


    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'word', 'category', 'translation'],
                name='unique_user_word_category_translation'
            )
        ]
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