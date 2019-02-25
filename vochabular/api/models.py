from django.db import models


class Chapter(models.Model):
    title = models.CharField(max_length=100)
    belongs_to = models.ForeignKey('self', on_delete=models.CASCADE)

    def __int__(self):
        return self.id


class WordGroup(models.Model):
    title = models.CharField(max_length=100)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)

    def __int__(self):
        return self.id


class ComponentType(models.Model):
    name = models.CharField(max_length=45)
    schema = models.TextField(max_length=100)

    def __int__(self):
        return self.id


class Component(models.Model):
    STATE_CHOICES = (
        ('0', 'state 1'),
        ('1', 'state 2'),
        ('2', 'state 3'),
        ('3', 'state 4'),
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
    text_id = models.ForeignKey(Text, on_delete=models.CASCADE)

    def __int__(self):
        return self.id
