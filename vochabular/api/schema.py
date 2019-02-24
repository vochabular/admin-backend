import graphene
from graphql_jwt.decorators import login_required

from graphene_django.types import DjangoObjectType
from api.models import Chapter
from api.models import WordGroup

class ChapterType(DjangoObjectType):
    class Meta:
        model = Chapter

class WordGroupType(DjangoObjectType):
    class Meta:
        model = WordGroup

class Query(graphene.ObjectType):
    all_chapters = graphene.List(ChapterType)
    all_wordGroups = graphene.List(WordGroupType)

    @login_required
    def resolve_all_chapters(self, info, **kwargs):
        return Chapter.objects.all()

    @login_required
    def resolve_all_wordGroups(self, info, **kwargs):
        return WordGroup.objects.all()








schema = graphene.Schema(query=Query)
