import graphene
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required

from api.models import Component, ComponentType


class ComponentTypeType(DjangoObjectType):
    class Meta:
        model = ComponentType
        filter_fields = ['base']
        interfaces = (graphene.relay.Node, )

    @classmethod
    def get_node(cls, info, id):
        return ComponentType.objects.get(id)


class Component_Type(DjangoObjectType):
    class Meta:
        model = Component
        filter_fields = ['state']
        interfaces = (graphene.relay.Node, )

    @classmethod
    def get_node(cls, info, id):
        return Component.objects.get(id)


class ComponentQuery(graphene.AbstractType):
    component_types = DjangoFilterConnectionField(ComponentTypeType)
    component_type = graphene.Field(type=ComponentTypeType, id=graphene.Int())
    components = DjangoFilterConnectionField(Component_Type)
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
    base = graphene.Boolean()
    icon = graphene.String(required=True)
    label = graphene.String(required=True)
    fk_parent_type_id = graphene.ID()


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


class ComponentInput(graphene.InputObjectType):
    data = graphene.String(required=True)
    state = graphene.String(required=True)
    fk_chapter_id = graphene.ID(required=True)
    fk_component_type_id = graphene.ID(required=True)


class IntroduceComponent(graphene.relay.ClientIDMutation):
    class Input:
        component_data = graphene.InputField(ComponentInput)

    component = graphene.Field(Component_Type)

    @classmethod
    def mutate_and_get_payload(cls, root, info, component_data):
        component = Component(**component_data)
        component.save()

        return IntroduceComponent(component=component)


class ComponentMutation(graphene.AbstractType):
    create_component = IntroduceComponent.Field()
