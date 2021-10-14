from django.contrib.auth.models import User
from django.db import models
# from django.urls import reverse
from django.shortcuts import resolve_url

# Create your models here.


class Photo(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user')
    text = models.TextField(blank=True)
    image = models.ImageField(upload_to='timeline_photo/%Y/%M/%d')
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    # admin 화면 표시 구현
    def __str__(self) -> str:
        return "text : " + self.text

    # 정렬 순서
    class Meta:
        ordering = ['-created']

    # detail 뷰를 만들게 되면 적극적으로 사용하라
    def get_absolute_url(self):
        # return reverse('photo:detail', args=[self.id])
        return resolve_url('photo:detail', self.id)


class Comment(models.Model):
    photo = models.ForeignKey(
        Photo, on_delete=models.CASCADE, related_name='comments')  # Photo 에서 comment를 가져올떄 이름
    writer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='writer')
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['updated']

    def __str__(self):
        return self.writer.username + " " + self.created.strftime("%Y-%m-%d %H:%M:%S")
