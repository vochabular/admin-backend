import graphene
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required

from api import models
from api.models import Word, WordAR, WordCH, WordDE, WordEN, WordFA, WordGroup


class WordGroupType(DjangoObjectType):
    class Meta:
        model = WordGroup


class WordType(DjangoObjectType):
    class Meta:
        model = Word

    @classmethod
    def get_node(cls, info, id):
        return WordType.objects.get(id)


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
    word = graphene.Field(type=WordType, id=graphene.Int())
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
    def resolve_word(self, info, id):
        return Word.objects.get(id=id)

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


class WordGroupInput(graphene.InputObjectType):
    fk_chapter_id = graphene.ID()
    title_de = graphene.String(required=True)
    title_ch = graphene.String(required=True)

class IntroduceWordGroup(graphene.relay.ClientIDMutation):
    class Input:
        word_group_data = graphene.InputField(WordGroupInput)
    
    wordGroup = graphene.Field(WordGroupType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, word_group_type):
        wordGroup = WordGroup(**word_group_type)
        wordGroup.save()

        return IntroduceWordGroup(wordGroup=wordGroup)

class IntroduceWord(graphene.relay.ClientIDMutation):
    word = graphene.Field(WordType)

    @classmethod
    def mutate_and_get_payload(cls, root, info):
        word = Word()
        word.save()
        cls.create_word_translations(word)

        return IntroduceWord(word=word)

    @classmethod
    def create_word_translations(cls, word):
        wordCH = WordCH(word=word)
        wordCH.save()
        wordEN = WordEN(word=word)
        wordEN.save()
        wordDE = WordDE(word=word)
        wordDE.save()
        wordFA = WordFA(word=word)
        wordFA.save()
        wordAR = WordAR(word=word)
        wordAR.save()


class TranslatedWordInput(graphene.InputObjectType):
    text = graphene.String(required=True)
    audio = graphene.String()
    example_sentence = graphene.String()


class UpdateTranslatedWord():
    class Input:
        word_id = graphene.ID()
        word_data = graphene.InputField(TranslatedWordInput)


class UpdateWordDE(UpdateTranslatedWord, graphene.relay.ClientIDMutation):
    word = graphene.Field(WordDEType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, word_data, word_id):
        return UpdateWordDE(word=mutate_word(word_data, word_id, "WordDE"))


class UpdateWordCH(UpdateTranslatedWord, graphene.relay.ClientIDMutation):
    word = graphene.Field(WordCHType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, word_data, word_id):
        return UpdateWordCH(word=mutate_word(word_data, word_id, "WordCH"))


class UpdateWordEN(UpdateTranslatedWord, graphene.relay.ClientIDMutation):
    word = graphene.Field(WordENType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, word_data, word_id):
        return UpdateWordEN(word=mutate_word(word_data, word_id, "WordEN"))


class UpdateWordFA(UpdateTranslatedWord, graphene.relay.ClientIDMutation):
    word = graphene.Field(WordFAType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, word_data, word_id):
        return UpdateWordFA(word=mutate_word(word_data, word_id, "WordFA"))


class UpdateWordAR(UpdateTranslatedWord, graphene.relay.ClientIDMutation):
    word = graphene.Field(WordARType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, word_data, word_id):
        return UpdateWordAR(word=mutate_word(word_data, word_id, "WordAR"))


class WordMutation(graphene.AbstractType):
    create_word = IntroduceWord.Field()
    update_de_word = UpdateWordDE.Field()
    update_ch_word = UpdateWordCH.Field()
    update_en_word = UpdateWordEN.Field()
    update_fa_word = UpdateWordFA.Field()
    update_ar_word = UpdateWordAR.Field()


def mutate_word(word_data, word_id, cls_name):
    word_cls = getattr(models, cls_name)
    word = word_cls(id=word_id)
    word.word_id = word_id
    word.text = word_data.text
    word.audio = word_data.audio
    word.example_sentence = word_data.example_sentence
    word.save()
    return word
