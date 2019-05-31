import graphene
from graphql_jwt.decorators import login_required
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType

from api.graphql.chapter import ChapterMutation, ChapterQuery
from api.graphql.component import ComponentTypeMutation, ComponentQuery, ComponentMutation
from api.graphql.word import WordMutation, WordQuery
from api.graphql.profile import ProfileMutation, ProfileQuery
from api.graphql.comment import CommentMutation, CommentQuery

from api.models import (
    Text,
    Translation,
    Media
)


class TextType(DjangoObjectType):
    class Meta:
        model = Text
        interfaces = (graphene.relay.Node, )
        filter_fields = ['fk_component_id']


class TranslationType(DjangoObjectType):
    class Meta:
        model = Translation
        interfaces = (graphene.relay.Node, )
        filter_fields = ['fk_text_id', 'language']


class MediaType(DjangoObjectType):
    class Meta:
        model = Media
        interfaces = (graphene.relay.Node, )
        filter_fields = ['fk_component_id']


class Query(graphene.ObjectType, ChapterQuery, ComponentQuery, WordQuery, ProfileQuery, CommentQuery):
    texts = DjangoFilterConnectionField(TextType)
    translations = DjangoFilterConnectionField(TranslationType)
    media = DjangoFilterConnectionField(MediaType)

    @login_required
    def resolve_texts(self, info, **kwargs):
        return Text.objects.all()

    @login_required
    def resolve_translations(self, info, **kwargs):
        return Translation.objects.all()

    @login_required
    def resolve_medias(self, info, **kwargs):
        return Media.objects.all()


class Mutation(graphene.ObjectType, ChapterMutation, ComponentTypeMutation, ComponentMutation, CommentMutation, WordMutation, ProfileMutation):
    class Meta:
        pass


schema = graphene.Schema(query=Query, mutation=Mutation)
