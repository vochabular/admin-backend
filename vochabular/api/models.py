from django.db import models

class Chapter(models.Model):
    title = models.CharField(max_length=100)
    belongs_to = models.ForeignKey('self', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class WordGroup(models.Model):
    title = models.CharField(max_length=100)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
