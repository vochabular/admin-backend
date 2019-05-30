import graphene, graphql_jwt
from django.contrib.auth.models import User
from graphql_jwt.decorators import login_required
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType

from api.graphql.chapter import ChapterMutation, ChapterQuery
from api.graphql.component import ComponentTypeMutation, ComponentQuery, ComponentMutation
from api.graphql.word import WordMutation, WordQuery

from api.models import (
    Text,
    Translation,
    Comment,
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


class CommentType(DjangoObjectType):
    class Meta:
        model = Comment
        interfaces = (graphene.relay.Node, )
        filter_fields = ['fk_text_id']

    @classmethod
    def get_node(cls, info, id):
        return Comment.objects.get(id)


class MediaType(DjangoObjectType):
    class Meta:
        model = Media
        interfaces = (graphene.relay.Node, )
        filter_fields = ['fk_component_id']


class UserType(DjangoObjectType):
    class Meta:
        model = User


class Query(graphene.ObjectType, ChapterQuery, ComponentQuery, WordQuery):
    texts = DjangoFilterConnectionField(TextType)
    translations = DjangoFilterConnectionField(TranslationType)
    comments = DjangoFilterConnectionField(CommentType)
    comment = graphene.Field(type=CommentType, id=graphene.Int())
    media = DjangoFilterConnectionField(MediaType)
    # Auth
    verify_token = graphql_jwt.Verify.Field()

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
    def resolve_medias(self, info, **kwargs):
        return Media.objects.all()


class UpdateUser(graphene.Mutation):
    class Arguments:
        firstname = graphene.String()
        lastname = graphene.String()

    user = graphene.Field(UserType)

    def mutate(self, info, firstname, lastname):
        user = info.context.user
        user.first_name = firstname
        user.last_name = lastname
        user.save()
        return UpdateUser(user=user)


class CommentInput(graphene.InputObjectType):
    comment = graphene.String(required=True)
    active =  graphene.Boolean(required=True)
    fk_text_id = graphene.ID(required=True)


class IntroduceComment(graphene.relay.ClientIDMutation):
    class Input:
        comment_data = graphene.InputField(CommentInput)

    comment = graphene.Field(CommentType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, comment_data):
        comment = Comment(**comment_data)
        comment.author_name = info.context.user
        comment.save()

        return IntroduceComment(comment=comment)


class CommentMutation(graphene.AbstractType):
    create_comment = IntroduceComment.Field()

class Mutation(graphene.ObjectType, ChapterMutation, ComponentTypeMutation, ComponentMutation, CommentMutation, WordMutation):
    update_user = UpdateUser.Field()
    
    class Meta:
        pass


schema = graphene.Schema(query=Query, mutation=Mutation)
