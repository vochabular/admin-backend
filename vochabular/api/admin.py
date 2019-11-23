from django.contrib import admin
from api.models import (
    Book,
    Chapter,
    ChapterTitle,
    Character,
    ComponentType,
    Component,
    Language,
    Text,
    Translation,
    Comment,
    Media,
    WordGroup,
    WordGroupTitle,
    Word,
    WordTranslation,
    Profile
)

admin.site.register(Book)
admin.site.register(Chapter)
admin.site.register(ChapterTitle)
admin.site.register(Character)
admin.site.register(ComponentType)
admin.site.register(Component)
admin.site.register(Language)
admin.site.register(Text)
admin.site.register(Translation)
admin.site.register(Comment)
admin.site.register(Media)
admin.site.register(WordGroup)
admin.site.register(WordGroupTitle)
admin.site.register(Word)
admin.site.register(WordTranslation)
admin.site.register(Profile)
