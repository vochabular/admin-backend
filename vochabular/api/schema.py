import graphene
from api.graphql.chapter import ChapterMutation, ChapterQuery
from api.graphql.component import ComponentTypeMutation, ComponentQuery, ComponentMutation
from api.graphql.word import WordMutation, WordQuery
from api.graphql.profile import ProfileMutation, ProfileQuery
from api.graphql.comment import CommentMutation, CommentQuery
from api.graphql.text import TextMutation, TextQuery
from api.graphql.media import MediaQuery
from api.graphql.language import LanguageQuery
from api.graphql.xml import XMLQuery


class Query(
    graphene.ObjectType,
    ChapterQuery,
    ComponentQuery,
    WordQuery,
    ProfileQuery,
    CommentQuery,
    TextQuery,
    MediaQuery,
    LanguageQuery,
    XMLQuery
):
    pass


class Mutation(
    graphene.ObjectType,
    ChapterMutation,
    ComponentTypeMutation,
    ComponentMutation,
    CommentMutation,
    WordMutation,
    ProfileMutation,
    TextMutation
):
    class Meta:
        pass


schema = graphene.Schema(query=Query, mutation=Mutation)
