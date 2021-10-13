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
