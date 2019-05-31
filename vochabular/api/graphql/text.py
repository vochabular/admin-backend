import graphene
from graphql_jwt.decorators import login_required
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType

from api.models import Text, Translation


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


class TextQuery(graphene.AbstractType):
    texts = DjangoFilterConnectionField(TextType)
    translations = DjangoFilterConnectionField(TranslationType)

    @login_required
    def resolve_texts(self, info, **kwargs):
        return Text.objects.all()

    @login_required
    def resolve_translations(self, info, **kwargs):
        return Translation.objects.all()


class TextMutation(graphene.AbstractType):
    create_text = CreateText.Field()
