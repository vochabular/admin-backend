import graphene
from graphql_jwt.decorators import login_required
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType

from api.models import Media


class MediaType(DjangoObjectType):
    class Meta:
        model = Media
        interfaces = (graphene.relay.Node, )
        filter_fields = ['fk_component_id']


class MediaQuery(graphene.AbstractType):
    media = DjangoFilterConnectionField(MediaType)

    @login_required
    def resolve_medias(self, info, **kwargs):
        return Media.objects.all()
