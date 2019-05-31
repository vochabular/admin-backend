import graphene
from graphql_jwt.decorators import login_required
from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from api.models import Comment


class CommentType(DjangoObjectType):
    class Meta:
        model = Comment
        interfaces = (graphene.relay.Node, )
        filter_fields = ['fk_component_id', 'active']

    @classmethod
    def get_node(cls, info, id):
        return Comment.objects.get(id)


class CommentQuery(graphene.AbstractType):
    comments = DjangoFilterConnectionField(CommentType)
    comment = graphene.Field(type=CommentType, id=graphene.Int())

    @login_required
    def resolve_comments(self, info, **kwargs):
        return Comment.objects.all()

    @login_required
    def resolve_comment(self, info, id):
        return Comment.objects.get(id=id)


class CommentInput(graphene.InputObjectType):
    text = graphene.String(required=True)
    active =  graphene.Boolean(required=True)
    fk_author_id = graphene.ID(required=True)
    context = graphene.String()
    fk_component_id = graphene.ID(required=True)
    fk_parent_comment_id = graphene.ID()


class IntroduceComment(graphene.relay.ClientIDMutation):
    class Input:
        comment_data = graphene.InputField(CommentInput)

    comment = graphene.Field(CommentType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, comment_data):
        comment = Comment(**comment_data)
        comment.save()

        return IntroduceComment(comment=comment)


class CommentMutation(graphene.AbstractType):
    create_comment = IntroduceComment.Field()
