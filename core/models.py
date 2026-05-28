from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    logtime = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=256, null=False, blank=False)

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name


class Book(models.Model):
    logtime = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=256, null=False, blank=False)
    publish_year = models.PositiveIntegerField(null=False, blank=False)
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, null=True, related_name="books"
    )

    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, null = True, related_name="books"
        )

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"
        ordering = ("name",)

    def __str__(self) -> str:
        return f'{self.author}: "{self.name}"'
    
class Comment(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author} - {self.book}"
    
