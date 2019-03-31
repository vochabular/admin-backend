from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


class Chapter(models.Model):
    title = models.CharField(max_length=100)
    fk_belongs_to = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    description = models.CharField(max_length=500)
    number = models.IntegerField()

    def __str__(self):
        return self.title


class ComponentType(models.Model):
    name = models.CharField(max_length=45)
    schema = models.TextField(max_length=100)

    def __str__(self):
        return self.name


class Component(models.Model):
    STATE_CHOICES = (
        ('C', 'creation'),
        ('R', 'in review'),
        ('U', 'to be updated'),
        ('T', 'to be translated'),
        ('F', 'final')
    )

    data = models.TextField(max_length=500)
    fk_chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    fk_component_type = models.ForeignKey(ComponentType, on_delete=models.CASCADE)
    state = models.CharField(max_length=1, choices=STATE_CHOICES, default='0')
    fk_component = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return 'Component:' + str(self.id)


class Translation(models.Model):
    language = models.CharField(max_length=45)
    text_field = models.CharField(max_length=45)
    valid = models.BooleanField()
    fk_text = models.ForeignKey('Text', on_delete=models.CASCADE)

    def __str__(self):
        return self.text_field


class Media(models.Model):
    type = models.CharField(max_length=45)
    url = models.CharField(max_length=255)
    fk_component = models.ForeignKey(Component, on_delete=models.CASCADE)

    def __str__(self):
        return 'ID :' + str(self.id) + 'Type: ' + self.type


class Text(models.Model):
    translatable = models.BooleanField()
    fk_component = models.ForeignKey(Component, on_delete=models.CASCADE)
    master_translation = models.OneToOneField(Translation, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return 'Text:' + str(self.id)


class Comment(models.Model):
    comment = models.CharField(max_length=500)
    active = models.BooleanField()
    author_name = models.ForeignKey(User, on_delete=models.CASCADE)
    written = models.DateTimeField(default=datetime.now, null=True, blank=True)
    fk_text = models.ForeignKey(Text, on_delete=models.CASCADE)

    def __str__(self):
        return self.comment


class WordGroup(models.Model):
    fk_chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    title_ch = models.CharField(max_length=200, blank=True)
    title_de = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return 'WordGroup:' + str(self.title_de)


class Word(models.Model):
    def __str__(self):
        return 'Word:' + str(self.id)


class Member(models.Model):
    fk_word = models.ForeignKey(Word, on_delete=models.CASCADE)
    fk_word_group = models.ForeignKey(WordGroup, on_delete=models.CASCADE)

    def __str__(self):
        return 'Member:' + str(self.id)


class WordCH(models.Model):
    text = models.CharField(max_length=40)
    word = models.OneToOneField(Word, on_delete=models.CASCADE)
    audio = models.CharField(max_length=255, null=True, blank=True)
    example_sentence = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return 'CH:' + self.text


class WordEN(models.Model):
    text = models.CharField(max_length=40)
    word = models.OneToOneField(Word, on_delete=models.CASCADE)
    audio = models.CharField(max_length=255, null=True, blank=True)
    example_sentence = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return 'EN:' + self.text


class WordDE(models.Model):
    text = models.CharField(max_length=40)
    word = models.OneToOneField(Word, on_delete=models.CASCADE)
    audio = models.CharField(max_length=255, null=True, blank=True)
    example_sentence = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return 'DE:' + self.text


class WordFA(models.Model):
    text = models.CharField(max_length=40)
    word = models.OneToOneField(Word, on_delete=models.CASCADE)
    audio = models.CharField(max_length=255, null=True, blank=True)
    example_sentence = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return 'FA:' + self.text


class WordAR(models.Model):
    text = models.CharField(max_length=40)
    word = models.OneToOneField(Word, on_delete=models.CASCADE)
    audio = models.CharField(max_length=255, null=True, blank=True)
    example_sentence = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return 'AR:' + self.text
