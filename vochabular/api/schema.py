import graphene
from graphql_jwt.decorators import login_required
from graphene_django.types import DjangoObjectType
from api.models import (
    Chapter,
    ComponentType,
    Component,
    Text,
    Translation,
    Comment,
    WordGroup,
    Word,
    Member,
    WordCH,
    WordEN,
    WordDE,
    WordFA,
    WordAR
)


class ChapterType(DjangoObjectType):
    class Meta:
        model = Chapter


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


class CommentType(DjangoObjectType):
    class Meta:
        model = Comment


class WordGroupType(DjangoObjectType):
    class Meta:
        model = WordGroup


class WordType(DjangoObjectType):
    class Meta:
        model = Word


class MemberType(DjangoObjectType):
    class Meta:
        model = Member


class WordCHType(DjangoObjectType):
    class Meta:
        model = WordCH


class WordENType(DjangoObjectType):
    class Meta:
        model = WordEN


class WordDEType(DjangoObjectType):
    class Meta:
        model = WordDE


class WordFAType(DjangoObjectType):
    class Meta:
        model = WordFA


class WordARType(DjangoObjectType):
    class Meta:
        model = WordAR


class Query(graphene.ObjectType):
    chapters = graphene.List(ChapterType)
    component_types = graphene.List(ComponentTypeType)
    components = graphene.List(Component_Type)
    texts = graphene.List(TextType)
    translations = graphene.List(TranslationType)
    comments = graphene.List(CommentType)
    word_groups = graphene.List(WordGroupType)
    words = graphene.List(WordType)
    members = graphene.List(MemberType)
    word_chs = graphene.List(WordCHType)
    word_ens = graphene.List(WordENType)
    word_des = graphene.List(WordDEType)
    word_fas = graphene.List(WordFAType)
    word_ars = graphene.List(WordARType)

    @login_required
    def resolve_chapters(self, info, **kwargs):
        return Chapter.objects.all()

    @login_required
    def resolve_component_types(self, info, **kwargs):
        return ComponentType.objects.all()

    @login_required
    def resolve_components(self, info, **kwargs):
        return Component.objects.all()

    @login_required
    def resolve_texts(self, info, **kwargs):
        return Text.objects.all()

    @login_required
    def resolve_translations(self, info, **kwargs):
        return Translation.objects.all()

    @login_required
    def resolve_comments(self, info, **kwargs):
        return Comment.objects.all()

    @login_required
    def resolve_word_groups(self, info, **kwargs):
        return WordGroup.objects.all()

    @login_required
    def resolve_words(self, info, **kwargs):
        return Word.objects.all()

    @login_required
    def resolve_members(self, info, **kwargs):
        return Member.objects.all()

    @login_required
    def resolve_word_chs(self, info, **kwargs):
        return WordCH.objects.all()

    @login_required
    def resolve_word_ens(self, info, **kwargs):
        return WordEN.objects.all()

    @login_required
    def resolve_word_des(self, info, **kwargs):
        return WordDE.objects.all()

    @login_required
    def resolve_word_fas(self, info, **kwargs):
        return WordFA.objects.all()

    @login_required
    def resolve_word_ars(self, info, **kwargs):
        return WordAR.objects.all()


schema = graphene.Schema(query=Query)
