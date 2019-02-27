from django.db import models


class Chapter(models.Model):
    title = models.CharField(max_length=100)
    belongs_to = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __int__(self):
        return self.id


class ComponentType(models.Model):
    name = models.CharField(max_length=45)
    schema = models.TextField(max_length=100)

    def __int__(self):
        return self.id


class Component(models.Model):
    STATE_CHOICES = (
        ('C', 'creation'),
        ('R', 'in review'),
        ('U', 'to be updated'),
        ('T', 'to be translated'),
        ('F', 'final')
    )

    data = models.TextField(max_length=500)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    componentType = models.ForeignKey(ComponentType, on_delete=models.CASCADE)
    state = models.CharField(max_length=1, choices=STATE_CHOICES, default='0')

    def __int__(self):
        return self.id


class Text(models.Model):
    translatable = models.BooleanField()
    component = models.ForeignKey(Component, on_delete=models.CASCADE)
    master_translation = models.IntegerField()

    def __int__(self):
        return self.id


class Translation(models.Model):
    language = models.CharField(max_length=45)
    text = models.CharField(max_length=45)
    valid = models.BooleanField()
    text_id = models.OneToOneField(Text, on_delete=models.CASCADE)

    def __int__(self):
        return self.id


class Comment(models.Model):
    comment = models.TextField(max_length=500)
    active = models.BooleanField()
    component = models.ForeignKey(Component, on_delete=models.CASCADE)

    def __int__(self):
        return self.id


class WordGroup(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)

    def __int__(self):
        return self.id


class Word(models.Model):

    def __int__(self):
        return self.id


class Member(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    word_group = models.ForeignKey(WordGroup, on_delete=models.CASCADE)

    def __int__(self):
        return self.id


class WordCH(models.Model):
    text = models.CharField(max_length=40)
    word = models.OneToOneField(Word, on_delete=models.CASCADE)

    def __int__(self):
        return self.id


class WordEN(models.Model):
    text = models.CharField(max_length=40)
    word = models.OneToOneField(Word, on_delete=models.CASCADE)

    def __int__(self):
        return self.id


class WordDE(models.Model):
    text = models.CharField(max_length=40)
    word = models.OneToOneField(Word, on_delete=models.CASCADE)

    def __int__(self):
        return self.id


class WordFA(models.Model):
    text = models.CharField(max_length=40)
    word = models.OneToOneField(Word, on_delete=models.CASCADE)

    def __int__(self):
        return self.id


class WordAR(models.Model):
    text = models.CharField(max_length=40)
    word = models.OneToOneField(Word, on_delete=models.CASCADE)

    def __int__(self):
        return self.id
