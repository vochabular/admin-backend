import graphene
from graphql_jwt.decorators import login_required
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType

from api.models import Text, Translation


class TextType(DjangoObjectType):
    class Meta:
        model = Text
        interfaces = (graphene.relay.Node, )
        filter_fields = [
            'fk_component_id',
            'translation__language',
            'translation__valid']


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


class TextInput(graphene.InputObjectType):
    translatable = graphene.Boolean(required=True)
    fk_component_id = graphene.ID(required=True)
    master_translation_id = graphene.ID()


class TranslationInput(graphene.InputObjectType):
    language = graphene.String(required=True)
    text_field = graphene.String(required=True)
    valid = graphene.Boolean(required=True)
    fk_text_id = graphene.ID(required=True)


class IntroduceText(graphene.relay.ClientIDMutation):
    class Input:
        text_data = graphene.InputField(TextInput)

    text = graphene.Field(TextType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, text_data):
        text = Text(**text_data)
        text.save()
        return IntroduceText(text=text)


class IntroduceTranslation(graphene.relay.ClientIDMutation):
    class Input:
        translation_data = graphene.InputField(TranslationInput)

    translation = graphene.Field(TextType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, translation_data):
        translation = Translation(**translation_data)
        translation.save()
        return IntroduceTranslation(translation=translation)


class UpdateText(graphene.relay.ClientIDMutation):
    class Input:
        text_id = graphene.ID()
        text_data = graphene.InputField(TextInput)

    text = graphene.Field(TextType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, text_data, text_id):
        text = Text.objects.get(pk=text_id)
        text.translatable = text_data.translatable
        text.fk_component_id = text_data.fk_component_id
        text.master_translation_id = text_data.master_translation_id
        text.save()
        return UpdateText(text=text)


class UpdateTranslation(graphene.relay.ClientIDMutation):
    class Input:
        translation_id = graphene.ID()
        translation_data = graphene.InputField(TranslationInput)

    translation = graphene.Field(TranslationType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, translation_data, translation_id):
        translation = Translation.objects.get(pk=translation_id)
        translation.text_field = translation_data.text_field
        translation.valid = translation_data.valid
        translation.save()
        return UpdateText(translation=translation)


class TextMutation(graphene.AbstractType):
    create_text = IntroduceText.Field()
    update_text = UpdateText.Field()
    create_translation = IntroduceTranslation.Field()
    update_translation = UpdateTranslation.Field()
