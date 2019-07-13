import django_filters, graphene
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required

from api.models import Chapter


class ChapterType(DjangoObjectType):
    translation_progress = graphene.Float()

    class Meta:
        model = Chapter
        interfaces = (graphene.relay.Node, )

    @classmethod
    def get_node(cls, info, id):
        return Chapter.objects.get(id)


class ChapterFilter(django_filters.FilterSet):
    class Meta:
        model = Chapter
        fields = {
            'fk_belongs_to': ['isnull'],
        }


class ChapterQuery(graphene.AbstractType):
    chapters = DjangoFilterConnectionField(
        ChapterType, filterset_class=ChapterFilter)
    chapter = graphene.Field(type=ChapterType, id=graphene.Int())

    def resolve_name(self, args, info):
        return self.instance.translation_progress

    @login_required
    def resolve_chapters(self, info, **kwargs):
        return Chapter.objects.all()

    @login_required
    def resolve_chapter(self, info, id):
        return Chapter.objects.get(id=id)


class ChapterInput(graphene.InputObjectType):
    titleCH = graphene.String(required=True)
    titleDE = graphene.String(required=True)
    fk_belongs_to_id = graphene.ID()
    description = graphene.String(required=True)
    number = graphene.Int(required=True)


class IntroduceChapter(graphene.relay.ClientIDMutation):
    class Input:
        chapter_data = graphene.InputField(ChapterInput)

    chapter = graphene.Field(ChapterType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, chapter_data):
        chapter = Chapter(**chapter_data)
        chapter.save()

        return IntroduceChapter(chapter=chapter)


class UpdateChapter(graphene.relay.ClientIDMutation):
    class Input:
        chapter_id = graphene.ID()
        chapter_data = graphene.InputField(ChapterInput)

    chapter = graphene.Field(ChapterType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, chapter_data, chapter_id):
        chapter = Chapter.objects.get(pk=chapter_id)
        chapter.titleCH = chapter_data.titleCH
        chapter.titleDE = chapter_data.titleDE
        chapter.fk_belongs_to_id = chapter_data.fk_belongs_to_id
        chapter.description = chapter_data.description
        chapter.number = chapter_data.number
        chapter.save()

        return UpdateChapter(chapter=chapter)


class ChapterMutation(graphene.AbstractType):
    create_chapter = IntroduceChapter.Field()
    update_chapter = UpdateChapter.Field()
