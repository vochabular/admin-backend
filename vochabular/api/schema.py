import graphene
from api.graphql.chapter import ChapterMutation, ChapterQuery


class Query(graphene.ObjectType, ChapterQuery):
    node = graphene.relay.Node.Field()


class Mutation(graphene.ObjectType, ChapterMutation):
    class Meta:
        pass


schema = graphene.Schema(query=Query, mutation=Mutation)
