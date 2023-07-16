from django.contrib import admin

from goals.models import GoalCategory, GoalComment, Goal


class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "title")
    readonly_fields = ("created", "updated")
    list_filter = ["is_deleted"]
    search_fields = ["title"]


class CommentsInLine(admin.StackedInline):
    model = GoalComment
    extra = 0


class GoalAdmin(admin.ModelAdmin):
    list_display = ("id", "description")
    search_fields = ("title", "description")
    readonly_fields = ("created", "updated")
    list_filter = ("status", "priority")
    inlines = [CommentsInLine]


admin.site.register(GoalCategory)
admin.site.register(Goal)
