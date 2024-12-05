from django.contrib import admin
from .models import Poll, Choice


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2 

# Customized Poll admin
@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ('question', 'created_at')  
    search_fields = ('question',)  
    list_filter = ('created_at',) 
    inlines = [ChoiceInline] 

# Optionally, register Choice separately for standalone management
@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('choice_text', 'poll', 'votes')  
    search_fields = ('choice_text', 'poll__question')  
    list_filter = ('poll',)  
