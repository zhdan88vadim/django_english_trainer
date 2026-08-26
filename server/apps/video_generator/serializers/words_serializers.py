from rest_framework import serializers
from server.apps.video_generator.models.models import Word
from server.apps.video_generator.models.word_answer import WordAnswer

class WordSerializer(serializers.ModelSerializer):
    """Сериализатор для слов"""
    success_rate = serializers.SerializerMethodField()
    total_attempts = serializers.SerializerMethodField()
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Word
        fields = [
            'id', 
            'word', 
            'translation', 
            'category',
            'category_name',
            'success_rate', 
            'total_attempts',
            'notes',
            'tags',
            'created_at'
        ]
    
    def get_success_rate(self, obj):
        """Процент правильных ответов"""
        answers = WordAnswer.objects.filter(word=obj)
        total = answers.count()
        
        if total == 0:
            return 0.0
        
        correct = answers.filter(is_correct=True).count()
        return round((correct / total) * 100, 2)
    
    def get_total_attempts(self, obj):
        """Общее количество попыток"""
        return WordAnswer.objects.filter(word=obj).count()

class AnswerSerializer(serializers.Serializer):
    """Сериализатор для ответа пользователя"""
    word_id = serializers.IntegerField()
    is_correct = serializers.BooleanField()

class AnswerResponseSerializer(serializers.Serializer):
    """Сериализатор для ответа API"""
    word_id = serializers.IntegerField()
    is_correct = serializers.BooleanField()
    success_rate = serializers.FloatField()
    total_attempts = serializers.IntegerField()
    streak = serializers.IntegerField()
    daily_stats = serializers.DictField(required=False)


class StatsSerializer(serializers.Serializer):
    """Сериализатор для статистики"""
    total_answers = serializers.IntegerField()
    correct = serializers.IntegerField()
    wrong = serializers.IntegerField()
    success_rate = serializers.FloatField()
    streak = serializers.IntegerField()
    total_words = serializers.IntegerField()
    practiced_today = serializers.IntegerField()