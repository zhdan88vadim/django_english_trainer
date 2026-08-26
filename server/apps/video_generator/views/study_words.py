# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from server.apps.video_generator.models.models import Word
from server.apps.video_generator.serializers.words_serializers import (
    WordSerializer, 
    AnswerSerializer, 
    AnswerResponseSerializer, 
    StatsSerializer
)
from server.apps.video_generator.services.words_services import (
    handle_answer, 
    get_words_for_practice, 
    get_stats
)


class PracticeWordsView(APIView):
    """Получить слова для практики"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        count = int(request.GET.get('count', 10))
        words = get_words_for_practice(request.user, count)
        serializer = WordSerializer(words, many=True)
        
        return Response({
            'words': serializer.data,
            'total': Word.objects.filter(user=request.user).count()
        })


class AnswerWordView(APIView):
    """Ответить на слово"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = AnswerSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            result = handle_answer(
                word_id=serializer.validated_data['word_id'],
                user=request.user,
                is_correct=serializer.validated_data['is_correct'],
            )
            
            response_serializer = AnswerResponseSerializer(result)
            return Response(response_serializer.data)
            
        except Word.DoesNotExist:
            return Response(
                {'error': 'Word not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class StatisticsView(APIView):
    """Получить статистику"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        stats = get_stats(request.user)
        serializer = StatsSerializer(stats)
        return Response(serializer.data)