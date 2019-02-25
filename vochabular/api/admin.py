from django.contrib import admin
from api.models import Chapter
from api.models import ComponentType
from api.models import Component
from api.models import Text
from api.models import Translation
from api.models import Comment
from api.models import WordGroup
from api.models import Word
from api.models import Member
from api.models import WordCH
from api.models import WordEN
from api.models import WordDE
from api.models import WordFA
from api.models import WordAR

admin.site.register(Chapter)
admin.site.register(ComponentType)
admin.site.register(Component)
admin.site.register(Text)
admin.site.register(Translation)
admin.site.register(Comment)
admin.site.register(WordGroup)
admin.site.register(Word)
admin.site.register(Member)
admin.site.register(WordCH)
admin.site.register(WordEN)
admin.site.register(WordDE)
admin.site.register(WordFA)
admin.site.register(WordAR)
