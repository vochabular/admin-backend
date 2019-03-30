import graphene
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required

from api.models import Component, ComponentType


class ComponentTypeType(DjangoObjectType):
    class Meta:
        model = ComponentType

    @classmethod
    def get_node(cls, info, id):
        return ComponentType.objects.get(id)


class Component_Type(DjangoObjectType):
    class Meta:
        model = Component

    @classmethod
    def get_node(cls, info, id):
        return Component.objects.get(id)


class ComponentQuery(graphene.AbstractType):
    component_types = graphene.List(ComponentTypeType)
    component_type = graphene.Field(type=ComponentTypeType, id=graphene.Int())
    components = graphene.List(Component_Type)
    component = graphene.Field(type=Component_Type, id=graphene.Int())

    @login_required
    def resolve_component_types(self, info, **kwargs):
        return ComponentType.objects.all()

    @login_required
    def resolve_component_type(self, info, id):
        return ComponentType.objects.get(id=id)

    @login_required
    def resolve_components(self, info, **kwargs):
        return Component.objects.all()

    @login_required
    def resolve_component(self, info, id):
        return Component.objects.get(id=id)


class ComponentTypeInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    schema = graphene.String(required=True)


class IntroduceComponentType(graphene.relay.ClientIDMutation):
    class Input:
        componentType_data = graphene.InputField(ComponentTypeInput)

    componentType = graphene.Field(ComponentTypeType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, componentType_data):
        componentType = ComponentType(**componentType_data)
        componentType.save()

        return IntroduceComponentType(componentType=componentType)


class ComponentTypeMutation(graphene.AbstractType):
    create_component_type = IntroduceComponentType.Field()
