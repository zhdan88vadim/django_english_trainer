from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
import random

from server.apps.video_generator.serializers.serializers import UserSerializer, GroupSerializer, WordSerializer, TextSerializer
from ..models import Word, Text

def home(request):
    return render(request, 'home.html')  # Uses the template

def about(request):
    return HttpResponse("<h1>About</h1><p>English Trainer Video Generator</p>")

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Group.objects.all().order_by("name")
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]


class WordViewSet(viewsets.ModelViewSet):
    """
    CRUD for user's words
    """
    serializer_class = WordSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Users can only see their own words
        return Word.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        # Automatically set the user when creating a word
        serializer.save(user=self.request.user)

        
    @action(detail=False, methods=['get'], url_path='random')
    def random_optimized(self, request):
        count = min(int(request.query_params.get('count', 5)), 50)
        
        # Get random IDs efficiently
        word_ids = list(self.get_queryset().values_list('id', flat=True))
        
        if not word_ids:
            return Response({'error': 'No words found'}, status=404)
        
        # Select random IDs
        selected_ids = random.sample(word_ids, min(count, len(word_ids)))
        
        # Fetch in single query
        random_words = Word.objects.filter(
            id__in=selected_ids,
            user=request.user
        )
        
        serializer = self.get_serializer(random_words, many=True)
        return Response({
            'count': len(random_words),
            'results': serializer.data
        })  

class TextViewSet(viewsets.ModelViewSet):
    """
    CRUD for user's texts
    """
    serializer_class = TextSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Users can only see their own texts
        return Text.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        # Automatically set the user when creating a text
        serializer.save(user=self.request.user)