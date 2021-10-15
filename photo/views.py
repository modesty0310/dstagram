from django.http.response import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404, render
from django.views.generic import UpdateView, CreateView, DeleteView, ListView, DetailView
from django.contrib.auth.decorators import login_required
from urllib.parse import urlparse

from config.settings import BASE_DIR
from .models import Photo, Comment
import os
from django.conf import settings

# Create your views here.


class PhotoList(ListView):
    model = Photo
    template_name_suffix = '_list'


class PhotoCreate(CreateView):
    model = Photo
    fields = ['text', 'image']
    template_name_suffix = '_create'
    success_url = '/'

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        if form.is_valid():
            form.instance.save()
            return redirect('/')
        else:
            return self.render_to_response({'form': form})


class PhotoUpdate(UpdateView):
    model = Photo
    fields = ['author', 'text', 'image']
    template_name_suffix = '_update'
    # success_url = '/'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.author != request.user:
            messages.warning(request, '수정할 권한이 없습니다.')
            return HttpResponseRedirect('/')
        else:
            return super(PhotoUpdate, self).dispatch(request, *args, **kwargs)


class PhotoDelete(DeleteView):
    model = Photo
    template_name_suffix = '_delete'
    success_url = '/'

    def dispatch(self, request, *args, **kwargs):
        object = self.get_object()
        if object.author != request.user:
            messages.warning(request, '삭제할 권한이 없습니다.')
            return HttpResponseRedirect('/')
        file_path = os.path.join(settings.BASE_DIR, object.image.path)
        print(file_path)
        os.remove(file_path)
        return super(PhotoDelete, self).dispatch(request, *args, **kwargs)


class PhotoDetail(DetailView):
    model = Photo
    template_name_suffix = '_detail'


@login_required
def comment_write(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    if request.method == "POST":
        text = request.POST.get('text')
        writer = request.user
        Comment.objects.create(photo=photo, writer=writer, text=text)
        return redirect('photo:detail', pk=photo.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user != comment.writer:
        messages.warning(request, '삭제할 권한이 없습니다.')
        return HttpResponseRedirect('/')
    else:
        comment.delete()
        return redirect('photo:detail', pk=comment.photo.pk)


@login_required
def like(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    if request.user in photo.like.all():
        photo.like.remove(request.user)
    else:
        photo.like.add(request.user)
    referer_url = request.META.get('HTTP_REFERER')
    path = urlparse(referer_url).path  # 원래 있던 위치로 리다이렉트
    return HttpResponseRedirect(path)


@login_required
def like_list(request):
    user = request.user
    like_post = user.like_photo.all()
    return render(request, 'photo/photo_list.html', {"object_list": like_post})


@login_required
def my_list(request):
    photo = Photo.objects.all()
    return render(request, 'photo/photo_mylist.html', {"photos": photo})
