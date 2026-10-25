from django.db import models
from django.utils import timezone


class Article(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    excerpt = models.TextField(blank=True)
    content = models.TextField(
        help_text='Usa ## para subtítulos y separa los párrafos con una línea en blanco.'
    )
    author = models.CharField(max_length=120)
    published_at = models.DateTimeField(default=timezone.now)
    is_published = models.BooleanField(default=False)
    image = models.ImageField(upload_to='articles/', blank=True)

    class Meta:
        ordering = ['-published_at']

    def __str__(self):
        return self.title


class AboutPage(models.Model):
    content = models.TextField(
        help_text='Separa los párrafos con una línea en blanco; usa ## o ### para subtítulos.'
    )

    class Meta:
        verbose_name = 'presentación del autor'
        verbose_name_plural = 'presentación del autor'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def __str__(self):
        return 'Sobre mí'
