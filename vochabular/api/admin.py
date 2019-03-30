from django.contrib import admin
from api.models import (
    Chapter,
    ComponentType,
    Component,
    Text,
    Translation,
    Comment,
    Media,
    WordGroup,
    Word,
    Member,
    WordCH,
    WordEN,
    WordDE,
    WordFA,
    WordAR
)

admin.site.register(Chapter)
admin.site.register(ComponentType)
admin.site.register(Component)
admin.site.register(Text)
admin.site.register(Translation)
admin.site.register(Comment)
admin.site.register(Media)
admin.site.register(WordGroup)
admin.site.register(Word)
admin.site.register(Member)
admin.site.register(WordCH)
admin.site.register(WordEN)
admin.site.register(WordDE)
admin.site.register(WordFA)
admin.site.register(WordAR)
