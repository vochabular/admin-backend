from django.contrib import admin
from api.models import Chapter
from api.models import WordGroup
from api.models import ComponentType
from api.models import Component
from api.models import Text
from api.models import Translation
from api.models import Comment

admin.site.register(Chapter)
admin.site.register(WordGroup)
admin.site.register(ComponentType)
admin.site.register(Component)
admin.site.register(Text)
admin.site.register(Translation)
admin.site.register(Comment)
