import graphene
import graphql_jwt
from graphql_jwt.decorators import login_required

class Mutations(graphene.ObjectType):
    verify_token = graphql_jwt.Verify.Field()

schema = graphene.Schema(mutation=Mutations)
