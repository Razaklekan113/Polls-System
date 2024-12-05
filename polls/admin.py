from django.contrib import admin
from .models import Poll, Choice

# Inline model for adding choices within the Poll admin
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2  # Default to 2 empty choices for convenience

# Customized Poll admin
@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ('question', 'created_at')  # Display these fields in the list view
    search_fields = ('question',)  # Add a search bar for questions
    list_filter = ('created_at',)  # Filter by creation date
    inlines = [ChoiceInline]  # Add inline choices for polls

# Optionally, register Choice separately for standalone management
@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('choice_text', 'poll', 'votes')  # Show related poll and vote count
    search_fields = ('choice_text', 'poll__question')  # Allow searching by choice text and poll question
    list_filter = ('poll',)  # Filter by associated poll
