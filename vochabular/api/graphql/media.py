import graphene
import boto3
import uuid
from graphql_jwt.decorators import login_required
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType
from django.conf import settings

from api.models import Media


class MediaType(DjangoObjectType):
    class Meta:
        model = Media
        interfaces = (graphene.relay.Node, )
        filter_fields = ['fk_component_id']


class MediaUrlType(graphene.ObjectType):
    data = graphene.String()
    url = graphene.String()

    def __init__(self, data, url):
        self.data = data
        self.url = url


class MediaQuery(graphene.AbstractType):
    media = DjangoFilterConnectionField(MediaType)
    media_url = graphene.Field(type=MediaUrlType, file_type=graphene.String())

    @login_required
    def resolve_medias(self, info, **kwargs):
        return Media.objects.all()

    @login_required
    def resolve_media_url(self, info, file_type):
        s3_client = boto3.client('s3')
        file_name = str(uuid.uuid4().hex[:20])
        bucket = settings.AWS_STORAGE_BUCKET_NAME
        presigned_post = s3_client.generate_presigned_post(
            Bucket = bucket,
            Key = file_name,
            Fields = {"acl": "public-read", "Content-Type": file_type},
            Conditions = [
                {"acl": "public-read"},
                {"Content-Type": file_type}
            ],
            ExpiresIn = 3600
        )
        return MediaUrlType(presigned_post, 'https://%s.s3.amazonaws.com/%s' % (bucket, file_name))
