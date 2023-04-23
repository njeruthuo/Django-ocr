from django.db import models


class Document(models.Model):
    title = models.CharField(max_length=200)
    file = models.ImageField(upload_to='images/')
    document_text = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title
