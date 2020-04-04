from graphene_django.types import DjangoObjectType
import django_filters, graphene
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required

from api.models import Language

class LanguageType(DjangoObjectType):
    class Meta:
        model = Language

class LanguageQuery(graphene.AbstractType):
    languages = graphene.List(LanguageType)
    language = graphene.Field(type=LanguageType, id=graphene.Int())

    @login_required
    def resolve_languages(self, info, **kwargs):
        return Language.objects.all()

    @login_required
    def resolve_language(self, info, id):
        return Language.objects.get(id=id)