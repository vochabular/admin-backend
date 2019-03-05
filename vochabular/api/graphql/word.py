import graphene
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required

from api.models import Word, WordAR, WordCH, WordDE, WordEN, WordFA, WordGroup


class WordGroupType(DjangoObjectType):
    class Meta:
        model = WordGroup


class WordType(DjangoObjectType):
    class Meta:
        model = Word


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


class WordQuery(graphene.AbstractType):
    word_groups = graphene.List(WordGroupType)
    words = graphene.List(WordType)
    words_ch = graphene.List(WordCHType)
    words_en = graphene.List(WordENType)
    words_de = graphene.List(WordDEType)
    words_fa = graphene.List(WordFAType)
    words_ar = graphene.List(WordARType)

    @login_required
    def resolve_word_groups(self, info, **kwargs):
        return WordGroup.objects.all()

    @login_required
    def resolve_words(self, info, **kwargs):
        return Word.objects.all()

    @login_required
    def resolve_words_ch(self, info, **kwargs):
        return WordCH.objects.all()

    @login_required
    def resolve_words_en(self, info, **kwargs):
        return WordEN.objects.all()

    @login_required
    def resolve_words_de(self, info, **kwargs):
        return WordDE.objects.all()

    @login_required
    def resolve_words_fa(self, info, **kwargs):
        return WordFA.objects.all()

    @login_required
    def resolve_words_ar(self, info, **kwargs):
        return WordAR.objects.all()
