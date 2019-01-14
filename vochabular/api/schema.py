import graphene
from graphql_jwt.decorators import login_required

from graphene_django.types import DjangoObjectType
from api.models import Chapter

class ChapterType(DjangoObjectType):
    class Meta:
        model = Chapter

class Query(graphene.ObjectType):
    all_chapters = graphene.List(ChapterType)

    @login_required
    def resolve_all_chapters(self, info, **kwargs):
        return Chapter.objects.all()

schema = graphene.Schema(query=Query)
