import graphene
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required

from api import models
from api.models import Word, WordTranslation, WordGroup


class WordGroupType(DjangoObjectType):
    class Meta:
        model = WordGroup
        interfaces = (graphene.relay.Node, )
        filter_fields = ['fk_chapter_id']

    @classmethod
    def get_node(cls, info, id):
        return WordGroupType.objects.get(id)


class WordType(DjangoObjectType):
    class Meta:
        model = Word

    @classmethod
    def get_node(cls, info, id):
        return WordType.objects.get(id)


class WordQuery(graphene.AbstractType):
    word_groups = DjangoFilterConnectionField(WordGroupType)
    word_group = graphene.Field(type=WordGroupType, id=graphene.ID())
    words = graphene.List(WordType)
    word = graphene.Field(type=WordType, id=graphene.Int())

    @login_required
    def resolve_word_groups(self, info, **kwargs):
        return WordGroup.objects.all()

    @login_required
    def resolve_word_group(self, info, id):
        return WordGroup.objects.get(id=id)

    @login_required
    def resolve_words(self, info, **kwargs):
        return Word.objects.all()

    @login_required
    def resolve_word(self, info, id):
        return Word.objects.get(id=id)


class WordGroupInput(graphene.InputObjectType):
    fk_chapter_id = graphene.ID(required=True)
    title_de = graphene.String(required=True)
    title_ch = graphene.String(required=True)
    words = graphene.List(graphene.ID)


class IntroduceWordGroup(graphene.relay.ClientIDMutation):
    class Input:
        word_group_data = graphene.InputField(WordGroupInput)

    word_group = graphene.Field(WordGroupType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, word_group_data):
        word_group = WordGroup(**word_group_data)
        word_group.save()

        return IntroduceWordGroup(word_group=word_group)


class UpdateWordGroup(graphene.relay.ClientIDMutation):
    class Input:
        word_group_id = graphene.ID()
        word_group_data = graphene.InputField(WordGroupInput)

    word_group = graphene.Field(WordGroupType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, word_group_data, word_group_id):
        word_group = WordGroup.objects.get(pk=word_group_id)
        word_group.fk_chapter_id = word_group_data.fk_chapter_id
        word_group.title_ch = word_group_data.title_ch
        word_group.title_de = word_group_data.title_de
        word_group.words.set(Word.objects.filter(pk__in=word_group_data.words))
        word_group.save()

        return UpdateWordGroup(word_group=word_group)


class IntroduceWord(graphene.relay.ClientIDMutation):
    word = graphene.Field(WordType)

    @classmethod
    def mutate_and_get_payload(cls, root, info):
        word = Word()
        word.save()

        return IntroduceWord(word=word)


class TranslatedWordInput(graphene.InputObjectType):
    text = graphene.String(required=True)
    audio = graphene.String()
    example_sentence = graphene.String()


class UpdateTranslatedWord():
    class Input:
        word_id = graphene.ID()
        word_data = graphene.InputField(TranslatedWordInput)


class WordMutation(graphene.AbstractType):
    create_word = IntroduceWord.Field()
    create_word_group = IntroduceWordGroup.Field()
    update_word_group = UpdateWordGroup.Field()
