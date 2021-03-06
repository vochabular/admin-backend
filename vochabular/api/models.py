from collections import defaultdict
from django.conf import settings
from django.db import models
from datetime import datetime
from django.contrib.postgres.fields import JSONField
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Language(BaseModel):
    id = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.id + ": " + self.name


class Book(BaseModel):
    number = models.IntegerField()

    def __str__(self):
        return "Book number: " + str(self.number)


class Character(BaseModel):
    GENDERS = (('f', 'Female'), ('m', 'Male'))
    formal_name = models.CharField(max_length=45)
    informal_name = models.CharField(max_length=45)
    gender = models.CharField(
        max_length=1, choices=GENDERS, default=GENDERS[0][0], null=True)
    title = models.CharField(max_length=45, null=True)
    speaker = models.CharField(max_length=45, null=True)
    fk_book = models.ForeignKey(
        Book, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        unique_together = [
            ['formal_name', 'fk_book'],
            ['informal_name', 'fk_book']
        ]

    def __str__(self):
        return self.formal_name


class Profile(BaseModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    roles = models.CharField(max_length=120)
    current_role = models.CharField(max_length=30)
    fk_language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True, related_name="profile_language")
    translator_languages = models.ManyToManyField("Language")
    event_notifications = models.BooleanField(default=True)
    setup_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username + ": " + self.firstname + " " + self.lastname


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


class Chapter(BaseModel):
    languages = models.ManyToManyField(Language, through="ChapterTitle")
    fk_belongs_to = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True)
    description = models.CharField(max_length=500)
    number = models.IntegerField()
    fk_book = models.ForeignKey(
        Book, on_delete=models.SET_NULL, null=True, blank=True)
    disable_children = models.BooleanField(default=False)

    @property
    def translation_progress(self):
        # Get translations from chapter
        total, valid = self.translations()
        progress = []
        for lang, total in total.items():
            if total == 0:
                progress.append({"lang": lang, "progress": 1})
            else:
                progress.append({"lang": lang, "progress": valid[lang]/total})

        return progress

    def translations(self):
        total = defaultdict(int)
        valid = defaultdict(int)
        chapters = Chapter.objects.all().filter(fk_belongs_to=self)
        if len(chapters) > 0:
            for chapter in chapters:
                # Get translations from subchapter
                stotal, svalid = chapter.translations()
                for lang, num in stotal.items():
                    total[lang] += num
                for lang, num in svalid.items():
                    valid[lang] += num
        else:
            for component in Component.objects.all().filter(fk_chapter=self):
                for text in Text.objects.all().filter(fk_component=component):
                    for translation in Translation.objects.all().filter(fk_text=text):
                        total[translation.language] += 1
                        if translation.valid:
                            valid[translation.language] += 1

        return (total, valid)

    def __str__(self):
        return self.description


class ChapterTitle(BaseModel):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)


class ComponentType(BaseModel):
    name = models.CharField(max_length=45)
    schema = JSONField()
    base = models.BooleanField(default=False)
    icon = models.CharField(max_length=100)
    label = models.CharField(max_length=45)
    fk_parent_type = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True)
    fk_frontend_widget = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True, related_name='frontend_widget')

    def __str__(self):
        return self.name

    def isTitle(self):
        return self.label == "title"

    def isText(self):
        return self.label == "text"

    def isDialogue(self):
        return self.label == "dialog"

    def isBubble(self):
        return self.label == "bubble"


class Component(BaseModel):
    STATE_CHOICES = (
        ('C', 'creation'),
        ('R', 'in review'),
        ('U', 'to be updated'),
        ('T', 'to be translated'),
        ('F', 'final')
    )

    data = JSONField()
    fk_chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    fk_component_type = models.ForeignKey(
        ComponentType, on_delete=models.CASCADE)
    state = models.CharField(max_length=1, choices=STATE_CHOICES, default='0')
    fk_component = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True)
    fk_locked_by = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, null=True, blank=True)
    locked_ts = models.DateTimeField(auto_now=True)
    order_in_chapter = models.PositiveIntegerField()

    # TODO(worxli): Make sure a component is not created on a chapter that has subchapters.

    def __str__(self):
        return 'Component:' + str(self.id)


class Translation(BaseModel):
    fk_language = models.ForeignKey(Language, on_delete=models.CASCADE)
    text_field = models.TextField(null=True)
    valid = models.BooleanField()
    fk_text = models.ForeignKey('Text', on_delete=models.CASCADE)

    class Meta:
        unique_together = ['fk_language', 'fk_text']

    def __str__(self):
        return self.text_field


class Media(BaseModel):
    type = models.CharField(max_length=45)
    url = models.CharField(max_length=255)
    fk_component = models.ForeignKey(Component, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return 'ID: ' + str(self.id) + 'Type: ' + self.type


class Text(BaseModel):
    translatable = models.BooleanField()
    fk_component = models.ForeignKey(Component, on_delete=models.CASCADE)
    placeholder = models.TextField(null=True)

    def __str__(self):
        return 'Text: ' + str(self.id)


class Comment(BaseModel):
    CONTEXT_CHOICES = (
        ('A', 'Approver'),
        ('C', 'ContentCreator'),
        ('T', 'Translator'),
        ('I', 'Illustrator')
    )

    text = models.CharField(max_length=500)
    active = models.BooleanField()
    context = models.CharField(
        max_length=1, choices=CONTEXT_CHOICES, null=True, blank=True)
    fk_author = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, null=True)
    written = models.DateTimeField(default=datetime.now, null=True, blank=True)
    fk_component = models.ForeignKey(Component, on_delete=models.CASCADE)
    fk_chapter = models.ForeignKey(Chapter, on_delete=models.SET_NULL, null=True)
    fk_parent_comment = models.ForeignKey(
        "Comment", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.text


class WordGroup(BaseModel):
    fk_chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, null=True)
    words = models.ManyToManyField("Word")
    titles = models.ManyToManyField(Language, through="WordGroupTitle")

    def __str__(self):
        return 'WordGroup:' + str(self.id)


class WordGroupTitle(BaseModel):
    wordGroup = models.ForeignKey(WordGroup, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)


class Word(BaseModel):
    def __str__(self):
        return 'Word:' + str(self.id)


class WordTranslation(BaseModel):
    text = models.CharField(max_length=40)
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    audio = models.CharField(max_length=255, null=True, blank=True)
    example_sentence = models.CharField(max_length=500, null=True, blank=True)
    fk_language = models.ForeignKey(Language, on_delete=models.CASCADE)

    def __str__(self):
        return 'Translated Word:' + self.text
