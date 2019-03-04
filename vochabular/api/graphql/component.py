import graphene
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required

from api.models import Component, ComponentType


class ComponentTypeType(DjangoObjectType):
    class Meta:
        model = ComponentType


class Component_Type(DjangoObjectType):
    class Meta:
        model = Component


class ComponentQuery(graphene.AbstractType):
    component_types = graphene.List(ComponentTypeType)
    components = graphene.List(Component_Type)

    @login_required
    def resolve_component_types(self, info, **kwargs):
        return ComponentType.objects.all()

    @login_required
    def resolve_components(self, info, **kwargs):
        return Component.objects.all()
