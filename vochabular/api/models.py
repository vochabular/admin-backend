from django.db import models

class Chapter(models.Model):
    title = models.CharField(max_length=100)
    text = models.CharField(max_length=100, null=True)
    belongs_to = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class WordGroup(models.Model):
    title = models.CharField(max_length=100)
    text = models.CharField(max_length=100, null=True)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
