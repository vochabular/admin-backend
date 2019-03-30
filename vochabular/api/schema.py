import graphene
from graphql_jwt.decorators import login_required
from graphene_django.types import DjangoObjectType
from api.graphql.chapter import ChapterMutation, ChapterQuery
from api.graphql.component import ComponentTypeMutation, ComponentQuery
from api.graphql.word import WordQuery

from api.models import (
    Text,
    Translation,
    Comment,
    Member
)


class TextType(DjangoObjectType):
    class Meta:
        model = Text


class TranslationType(DjangoObjectType):
    class Meta:
        model = Translation


class CommentType(DjangoObjectType):
    class Meta:
        model = Comment

    @classmethod
    def get_node(cls, info, id):
        return Comment.objects.get(id)


class MemberType(DjangoObjectType):
    class Meta:
        model = Member


class Query(graphene.ObjectType, ChapterQuery, ComponentQuery, WordQuery):
    texts = graphene.List(TextType)
    translations = graphene.List(TranslationType)
    comments = graphene.List(CommentType)
    comment = graphene.Field(type=CommentType, id=graphene.Int())
    members = graphene.List(MemberType)

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
    def resolve_comment(self, info, id):
        return Comment.objects.get(id=id)

    @login_required
    def resolve_members(self, info, **kwargs):
        return Member.objects.all()


class Mutation(graphene.ObjectType, ChapterMutation, ComponentTypeMutation):
    class Meta:
        pass


schema = graphene.Schema(query=Query, mutation=Mutation)
