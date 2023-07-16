from django.contrib import admin

from goals.models import GoalCategory


class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "title")
    readonly_fields = ("created", "updated")
    list_filter = ["is_deleted"]
    search_fields = ["title"]


class GoalAdmin(admin.ModelAdmin):
    list_display = ["user", "category", "title", "status", "priority", "due_date"]
    list_filter = ["status", "priority", "due_date"]
    readonly_fields = ["created", "updated"]


class GoalCommentAdmin(admin.ModelAdmin):
    list_display = ["goal", "user", "created", "updated"]
    search_fields = ["goal__title"]
    readonly_fields = ["created", "updated"]


class BoardAdmin(admin.ModelAdmin):
    list_display = ["title", ]


class BoardParticipantAdmin(admin.ModelAdmin):
    list_display = ["board", "user", "role"]


admin.site.register(GoalCategory)
