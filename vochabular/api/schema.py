import graphene, graphql_jwt
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
    Media,
    Profile
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


class ProfileType(DjangoObjectType):
    class Meta:
        model = Profile

    @classmethod
    def get_node(cls, info, id):
        return Profile.objects.get(id)


class Query(graphene.ObjectType, ChapterQuery, ComponentQuery, WordQuery):
    texts = DjangoFilterConnectionField(TextType)
    translations = DjangoFilterConnectionField(TranslationType)
    comments = DjangoFilterConnectionField(CommentType)
    comment = graphene.Field(type=CommentType, id=graphene.Int())
    media = DjangoFilterConnectionField(MediaType)
    # Auth
    verify_token = graphql_jwt.Verify.Field()
    profile = graphene.Field(type=ProfileType, id=graphene.Int())

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


class UpdateProfile(graphene.relay.ClientIDMutation):
    class Arguments:
        firstname = graphene.String()
        lastname = graphene.String()

    profile = graphene.Field(ProfileType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, profile_data, profile_id):
        profile = Profile.objects.get(pk=profile_id)
        profile.first_name = profile_data.firstname
        profile.last_name = profile_data.lastname
        profile.role = profile_data.role
        profile.language = profile_data.language
        profile.translator_languages = profile_data.translator_languages
        profile.event_notifications = profile_data.event_notifications
        profile.setup_completed = profile_data.setup_completed
        profile.save()
        return UpdateProfile(profile=profile)


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
    update_user = UpdateProfile.Field()
    
    class Meta:
        pass


schema = graphene.Schema(query=Query, mutation=Mutation)
