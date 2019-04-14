import graphene
import graphql_jwt
from django.contrib.auth.models import User
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required


class Query(graphene.ObjectType):
    verify_token = graphql_jwt.Verify.Field()


class UserType(DjangoObjectType):
    class Meta:
        model = User


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


class Mutation(graphene.ObjectType):
    update_user = UpdateUser.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
