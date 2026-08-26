# services/words_services.py
from django.utils import timezone
from django.db import transaction
from django.db.models import Count, Q, F

from server.apps.video_generator.models.models import Word
from server.apps.video_generator.models.word_answer import WordAnswer
from server.apps.video_generator.models.dayly_progress import DailyProgress


def handle_answer(word_id, user, is_correct):
    """Обработка ответа пользователя"""
    with transaction.atomic():
        word = Word.objects.get(id=word_id, user=user)
        
        # Сохраняем ответ
        WordAnswer.objects.create(
            word=word,
            user=user,
            is_correct=is_correct,
        )
        
        # Обновляем дневную статистику
        today = timezone.now().date()
        daily, _ = DailyProgress.objects.get_or_create(
            user=user,
            date=today,
            defaults={
                'words_practiced': 0,
                'correct_answers': 0,
                'wrong_answers': 0,
                'new_words': 0
            }
        )
        
        daily.words_practiced += 1
        if is_correct:
            daily.correct_answers += 1
        else:
            daily.wrong_answers += 1
        daily.save()
        
        # Получаем статистику слова
        total_answers = WordAnswer.objects.filter(word=word).count()
        correct_answers = WordAnswer.objects.filter(word=word, is_correct=True).count()
        success_rate = round((correct_answers / total_answers * 100), 2) if total_answers > 0 else 0
        
        return {
            'word_id': word.id,
            'is_correct': is_correct,
            'success_rate': success_rate,
            'total_attempts': total_answers,
            'streak': get_streak(user),
            'daily_stats': {
                'practiced': daily.words_practiced,
                'correct': daily.correct_answers,
                'wrong': daily.wrong_answers,
                'success_rate': daily.success_rate,
            }
        }


def get_streak(user):
    """Текущая серия правильных ответов"""
    streak = 0
    for answer in WordAnswer.objects.filter(user=user).order_by('-answered_at'):
        if answer.is_correct:
            streak += 1
        else:
            break
    return streak


def get_words_for_practice(user, count=10):
    """Слова для практики"""
    words = Word.objects.filter(user=user).annotate(
        total=Count('answers'),
        correct=Count('answers', filter=Q(answers__is_correct=True))
    )
    
    # Сначала сложные (меньше 50% правильных), потом новые, потом остальные
    hard = words.filter(
        total__gt=0, 
        correct__lt=F('total') * 0.5
    )[:count//2]
    
    new_words = words.filter(total=0)[:count//4]
    
    rest = words.exclude(
        id__in=[w.id for w in hard] + [w.id for w in new_words]
    )[:count - len(hard) - len(new_words)]
    
    return list(hard) + list(new_words) + list(rest)


def get_stats(user):
    """Статистика пользователя"""
    answers = WordAnswer.objects.filter(user=user)
    total = answers.count()
    correct = answers.filter(is_correct=True).count()
    wrong = total - correct
    
    today = timezone.now().date()
    practiced_today = DailyProgress.objects.filter(user=user, date=today).first()
    
    return {
        'total_answers': total,
        'correct': correct,
        'wrong': wrong,
        'success_rate': round((correct / total * 100), 2) if total > 0 else 0,
        'streak': get_streak(user),
        'total_words': Word.objects.filter(user=user).count(),
        'practiced_today': practiced_today.words_practiced if practiced_today else 0,
    }