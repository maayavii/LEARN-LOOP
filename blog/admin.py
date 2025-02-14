from django.contrib import admin
from .models import Comment, Post

admin.site.register(Post)
admin.site.register(Comment)

from .models import UserContribution

@admin.register(UserContribution)
class UserContributionAdmin(admin.ModelAdmin):
    list_display = ('user', 'period_start', 'period_end', 'total_posts', 'total_comments', 'contribution_score')
    list_filter = ('period_start', 'period_end')
    search_fields = ('user__username',)
    ordering = ('-contribution_score',)