from django.contrib import admin

from goals.models import GoalCategory, GoalComment, Goal, BoardParticipant, Board


class ParticipantsInLine(admin.TabularInline):
    model = BoardParticipant
    extra = 0

    def get_queryset(self, request):
        return super().get_queryset(request).exclude(role=BoardParticipant.Role.owner)


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "participants_count", "is_deleted")
    list_display_links = ["title"]
    list_filter = ["is_deleted"]
    search_fields = ["title"]
    inlines = [ParticipantsInLine]

    def participants_count(self, obj: Board) -> int:
        return obj.participants.exclude(role=BoardParticipant.Role.owner).count()


@admin.register(GoalCategory)
class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "title")
    readonly_fields = ("created", "updated")
    list_filter = ["is_deleted"]
    search_fields = ["title"]


class CommentsInLine(admin.StackedInline):
    model = GoalComment
    extra = 0


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ("id", "description")
    search_fields = ("title", "description")
    readonly_fields = ("created", "updated")
    list_filter = ("status", "priority")
    inlines = [CommentsInLine]
