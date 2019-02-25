import graphene
from graphql_jwt.decorators import login_required
from graphene_django.types import DjangoObjectType
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
    all_chapters = graphene.List(ChapterType)
    all_component_types = graphene.List(ComponentTypeType)
    all_components = graphene.List(Component_Type)
    all_texts = graphene.List(TextType)
    all_translations = graphene.List(TranslationType)
    all_comments = graphene.List(CommentType)
    all_word_groups = graphene.List(WordGroupType)
    all_words = graphene.List(WordType)
    all_members = graphene.List(MemberType)
    all_word_chs = graphene.List(WordCHType)
    all_word_ens = graphene.List(WordENType)
    all_word_des = graphene.List(WordDEType)
    all_word_fas = graphene.List(WordFAType)
    all_word_ars = graphene.List(WordARType)

    @login_required
    def resolve_all_chapters(self, info, **kwargs):
        return Chapter.objects.all()

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

    @login_required
    def resolve_all_comments(self, info, **kwargs):
        return Comment.objects.all()

    @login_required
    def resolve_all_word_groups(self, info, **kwargs):
        return WordGroup.objects.all()

    @login_required
    def resolve_all_words(self, info, **kwargs):
        return Word.objects.all()

    @login_required
    def resolve_all_members(self, info, **kwargs):
        return Member.objects.all()

    @login_required
    def resolve_all_word_chs(self, info, **kwargs):
        return WordCH.objects.all()

    @login_required
    def resolve_all_word_ens(self, info, **kwargs):
        return WordEN.objects.all()

    @login_required
    def resolve_all_word_des(self, info, **kwargs):
        return WordDE.objects.all()

    @login_required
    def resolve_all_word_fas(self, info, **kwargs):
        return WordFA.objects.all()

    @login_required
    def resolve_all_word_ars(self, info, **kwargs):
        return WordAR.objects.all()

schema = graphene.Schema(query=Query)
