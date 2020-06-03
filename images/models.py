from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse

class Image(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='images_created', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    url = models.URLField()
    image = models.ImageField(upload_to='images/%Y/%m/%d')
    description = models.TextField(blank=True)
    created = models.DateField(auto_now_add=True, db_index=True)
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                        related_name='images_liked',
                                        blank=True)
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Image, self).save(*args,**kwargs)
    def get_absolute_url(self):
        return reverse('images:detail', args=[self.id, self.slug])

class Comment(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE, verbose_name='Obiavlenie')
    author = models.CharField(max_length=30, verbose_name='Author')
    content = models.TextField(verbose_name="Soderjanie")
    is_active = models.BooleanField(default=True, db_index=True, verbose_name='Show to display?')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Created")

    class Meta:
        verbose_name_plural = 'Комментарии'
        verbose_name = 'Комментарий'
        ordering = ['created_at']
