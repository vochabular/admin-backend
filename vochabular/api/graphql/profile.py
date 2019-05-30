import graphene
import graphql_jwt
from graphene_django.types import DjangoObjectType

from api.models import Profile


class ProfileType(DjangoObjectType):
    class Meta:
        model = Profile

    @classmethod
    def get_node(cls, info, username):
        return Profile.objects.get(user__username=username)


class ProfileQuery(graphene.AbstractType):
    profile = graphene.Field(type=ProfileType, username=graphene.String())
    # Auth
    verify_token = graphql_jwt.Verify.Field()


class ProfileInput(graphene.InputObjectType):
    firstname = graphene.String()
    lastname = graphene.String()
    roles = graphene.String()
    current_role = graphene.String()
    language = graphene.String()
    translator_languages = graphene.String()
    event_notifications = graphene.Boolean()
    setup_completed = graphene.Boolean()


class UpdateProfile(graphene.relay.ClientIDMutation):
    class Input:
        username = graphene.ID()
        profile_data = graphene.InputField(ProfileInput)

    profile = graphene.Field(ProfileType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, profile_data, username):
        profile = Profile.objects.get(user__username=username)
        profile.firstname = profile_data.firstname
        profile.lastname = profile_data.lastname
        profile.roles = profile_data.roles
        profile.current_role = profile_data.current_role
        profile.language = profile_data.language
        profile.translator_languages = profile_data.translator_languages
        profile.event_notifications = profile_data.event_notifications
        profile.setup_completed = profile_data.setup_completed
        profile.save()
        return UpdateProfile(profile=profile)


class ProfileMutation(graphene.AbstractType):
    update_profile = UpdateProfile.Field()
