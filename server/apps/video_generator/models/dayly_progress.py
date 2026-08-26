# models/daily_progress.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class DailyProgress(models.Model):
    """
    Ежедневный прогресс пользователя
    """
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='daily_progress'
    )
    date = models.DateField(default=timezone.now)
    
    # Статистика за день
    words_practiced = models.IntegerField(default=0, help_text="Слов попрактиковано")
    correct_answers = models.IntegerField(default=0, help_text="Правильных ответов")
    wrong_answers = models.IntegerField(default=0, help_text="Неправильных ответов")
    new_words = models.IntegerField(default=0, help_text="Новых слов добавлено")
    
    # Дополнительно
    streak = models.IntegerField(default=0, help_text="Текущая серия")
    best_streak = models.IntegerField(default=0, help_text="Лучшая серия")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'date']
        ordering = ['-date']
        indexes = [
            models.Index(fields=['user', 'date']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.date}"
    
    @property
    def total_answers(self):
        """Всего ответов за день"""
        return self.correct_answers + self.wrong_answers
    
    @property
    def success_rate(self):
        """Процент правильных ответов за день"""
        total = self.correct_answers + self.wrong_answers
        if total == 0:
            return 0.0
        return round((self.correct_answers / total) * 100, 2)
    
    @property
    def is_completed(self):
        """Достигнут ли дневной лимит (например, 20 слов)"""
        return self.words_practiced >= 20
    
    def add_answer(self, is_correct):
        """Добавить ответ"""
        self.words_practiced += 1
        if is_correct:
            self.correct_answers += 1
        else:
            self.wrong_answers += 1
        self.save()
    
    def update_streak(self, streak):
        """Обновить серию"""
        self.streak = streak
        if streak > self.best_streak:
            self.best_streak = streak
        self.save()
    
    @classmethod
    def get_or_create_today(cls, user):
        """Получить или создать запись за сегодня"""
        today = timezone.now().date()
        return cls.objects.get_or_create(
            user=user,
            date=today,
            defaults={
                'words_practiced': 0,
                'correct_answers': 0,
                'wrong_answers': 0,
                'new_words': 0,
                'streak': 0,
                'best_streak': 0
            }
        )
    
    @classmethod
    def get_weekly_stats(cls, user, days=7):
        """Получить статистику за последние N дней"""
        from datetime import timedelta
        start_date = timezone.now().date() - timedelta(days=days)
        
        return cls.objects.filter(
            user=user,
            date__gte=start_date
        ).order_by('date')
    
    @classmethod
    def get_monthly_stats(cls, user, days=30):
        """Получить статистику за последние N дней"""
        from datetime import timedelta
        start_date = timezone.now().date() - timedelta(days=days)
        
        return cls.objects.filter(
            user=user,
            date__gte=start_date
        ).order_by('date')