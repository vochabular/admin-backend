import graphene
from graphql_jwt.decorators import login_required
from graphene_django.types import DjangoObjectType
from api.models import Chapter
from api.models import WordGroup
from api.models import ComponentType
from api.models import Component
from api.models import Text
from api.models import Translation


class ChapterType(DjangoObjectType):
    class Meta:
        model = Chapter


class WordGroupType(DjangoObjectType):
    class Meta:
        model = WordGroup


class ComponentTypeType(DjangoObjectType):
    class Meta:
        model = ComponentType


class Component_Type(DjangoObjectType):
    class Meta:
        model = Component


class TextType(DjangoObjectType):
    class Meta:
        model = Text


class TranslationType(DjangoObjectType):
    class Meta:
        model = Translation


class Query(graphene.ObjectType):
    all_chapters = graphene.List(ChapterType)
    all_word_groups = graphene.List(WordGroupType)
    all_component_types = graphene.List(ComponentTypeType)
    all_components = graphene.List(Component_Type)
    all_texts = graphene.List(TextType)
    all_translations = graphene.List(TranslationType)

    @login_required
    def resolve_all_chapters(self, info, **kwargs):
        return Chapter.objects.all()

    @login_required
    def resolve_all_word_groups(self, info, **kwargs):
        return WordGroup.objects.all()

    @login_required
    def resolve_all_component_types(self, info, **kwargs):
        return ComponentType.objects.all()

    @login_required
    def resolve_all_components(self, info, **kwargs):
        return Component.objects.all()

    @login_required
    def resolve_all_texts(self, info, **kwargs):
        return Text.objects.all()

    @login_required
    def resolve_all_translations(self, info, **kwargs):
        return Translation.objects.all()


schema = graphene.Schema(query=Query)
