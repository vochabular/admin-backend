from django.contrib import admin
from api.models import (
    Chapter,
    ComponentType,
    Component,
    Language,
    Text,
    Translation,
    Comment,
    Media,
    WordGroup,
    Word,
    WordTranslation,
    Profile
)

admin.site.register(Chapter)
admin.site.register(ComponentType)
admin.site.register(Component)
admin.site.register(Language)
admin.site.register(Text)
admin.site.register(Translation)
admin.site.register(Comment)
admin.site.register(Media)
admin.site.register(WordGroup)
admin.site.register(Word)
admin.site.register(WordTranslation)
admin.site.register(Profile)
