from django.db import models
from django.db.models import Manager
from django.contrib.auth.models import User
from django.db.models.query import QuerySet


class Document(models.Model):
    title = models.CharField(max_length=200)
    file = models.ImageField(upload_to='images/', default=None)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    document_text = models.TextField(default='')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title


class Page(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    file = models.ImageField(upload_to='images/')
    document_text = models.TextField()

# class Document(models.Model):
#     title = models.CharField(max_length=200)
#     owner = models.ForeignKey(User, on_delete=models.CASCADE)
#     uploaded_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.title


# class Page(models.Model):
#     document = models.ForeignKey(Document, on_delete=models.CASCADE)
#     file = models.ImageField(upload_to='images/')
#     document_text = models.TextField()

#     def __str__(self):
#         return f"Page {self.pk} of {self.document.title}"
