import graphene
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required

from api.models import Chapter


class ChapterType(DjangoObjectType):
    class Meta:
        model = Chapter

    @classmethod
    def get_node(cls, info, id):
        return Chapter.objects.get(id)


class ChapterQuery(graphene.AbstractType):
    chapters = graphene.List(ChapterType)
    chapter = graphene.Field(type=ChapterType, id=graphene.Int())

    @login_required
    def resolve_chapters(self, info, **kwargs):
        return Chapter.objects.all()

    @login_required
    def resolve_chapter(self, info, id):
        return Chapter.objects.get(id=id)


class ChapterInput(graphene.InputObjectType):
    title = graphene.String(required=True)
    fk_belongs_to_id = graphene.ID(required=True)
    description = graphene.String(required=True)
    number = graphene.Float(required=True)

class IntroduceChapter(graphene.relay.ClientIDMutation):
    class Input:
        chapter_data = graphene.InputField(ChapterInput)

    chapter = graphene.Field(ChapterType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, chapter_data):
        chapter = Chapter(**chapter_data)
        chapter.save()

        return IntroduceChapter(chapter=chapter)


class ChapterMutation(graphene.AbstractType):
    create_chapter = IntroduceChapter.Field()
