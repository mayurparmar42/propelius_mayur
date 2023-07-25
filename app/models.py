from django.db import models

# Create your models here.


class NoteDetails(models.Model):
    noteId = models.AutoField(primary_key=True)
    title = models.CharField(blank=True, null= True, max_length=100)
    content = models.TextField(blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.noteId)