from __future__ import unicode_literals

from django.utils.safestring import mark_safe
from markdown_deux import markdown

from django.db import models
from django.utils import timezone

class Post (models.Model):
    author = models.ForeignKey('auth.user')
    title = models.CharField(max_length = 200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date=timezone.now()

    def __str__(self):
        return self.title

    def get_markdown(self): #za markdown teksta, pretvaramo sve ovdje i iz template-a pozivamo
        text = self.text
        return mark_safe(markdown(text))

class Comment(models.Model):
    post = models.ForeignKey('blog.Post', related_name='comments')
    author = models.ForeignKey('auth.user')
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text

class Status(models.Model):
    author = models.ForeignKey('auth.user')
    status = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def approve(self):
        self.approved_status = True
        self.save()
        
    def __str__(self):
        return self.status
