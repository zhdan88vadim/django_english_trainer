from django.contrib.auth.models import Group, User
from rest_framework import serializers
from .models import Word, Text

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "groups"]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ["url", "name"]

class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = ['id', 'word', 'translation', 'created_at']
        read_only_fields = ['id', 'created_at']

class TextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text
        fields = ['id', 'title', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']        