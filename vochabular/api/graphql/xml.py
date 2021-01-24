import boto3
import os
import uuid
import graphene
from django.conf import settings
from graphql_jwt.decorators import login_required
from api.xml.generator import XMLGenerator
from api.models import Chapter


class GeneratedXMLType(graphene.ObjectType):
    path = graphene.String()


class XMLQuery(graphene.AbstractType):
    chapterXML = graphene.Field(type=GeneratedXMLType, id=graphene.ID())

    @login_required
    def resolve_chapterXML(self, info, id):
        chapter = Chapter.objects.get(id=id)
        return genChapterXML(chapter)

def genChapterXML(chapter: Chapter):
    xml = XMLGenerator().createChapter(chapter)
    return GeneratedXMLType(path=saveXML(xml))

def saveXML(xml):
    access_key = os.environ.get('AWS_ACCESS_KEY_ID')
    secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    s3 = boto3.resource('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    bucket = s3.Bucket(bucket_name)

    file_name = str(uuid.uuid4()) + ".xml"
    bucket.put_object(Key=file_name, Body=xml)
    return 'https://%s.s3.amazonaws.com/%s' % (bucket_name, file_name)
