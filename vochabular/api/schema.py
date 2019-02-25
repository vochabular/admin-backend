import graphene
from graphql_jwt.decorators import login_required
from graphene_django.types import DjangoObjectType
from api.models import Chapter
from api.models import WordGroup
from api.models import ComponentType
from api.models import Component


class ChapterType(DjangoObjectType):
    class Meta:
        model = Chapter


class WordGroupType(DjangoObjectType):
    class Meta:
        model = WordGroup


class ComponentTypeType(DjangoObjectType):
    class Meta:
        model = ComponentType


class ComponentType(DjangoObjectType):
    class Meta:
        model = Component


class Query(graphene.ObjectType):
    all_chapters = graphene.List(ChapterType)
    all_wordGroups = graphene.List(WordGroupType)
    all_componentTypes = graphene.List(ComponentTypeType)
    all_components = graphene.List(ComponentType)

    @login_required
    def resolve_all_chapters(self, info, **kwargs):
        return Chapter.objects.all()

    @login_required
    def resolve_all_wordGroups(self, info, **kwargs):
        return WordGroup.objects.all()

    @login_required
    def resolve_all_componentTypes(self, info, **kwargs):
        return ComponentType.objects.all()

    @login_required
    def resolve_all_components(self, info, **kwargs):
        return Component.objects.all()


schema = graphene.Schema(query=Query)
