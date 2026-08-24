from django.contrib import admin
from server.apps.video_generator.models import Word, Text

@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ['word', 'translation', 'user', 'created_at']
    list_filter = ['user', 'created_at']
    search_fields = ['word', 'translation']

@admin.register(Text)
class TextAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'created_at', 'updated_at']
    list_filter = ['user', 'created_at']
    search_fields = ['title', 'content']