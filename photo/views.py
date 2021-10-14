from django.http.response import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import UpdateView, CreateView, DeleteView, ListView, DetailView
from django.urls import reverse
from .models import Photo, Comment
from .form import CommentForm

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
        return super(PhotoDelete, self).dispatch(request, *args, **kwargs)


class PhotoDetail(DetailView):
    model = Photo
    template_name_suffix = '_detail'


def comment_write(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.photo = photo
            comment.save()
            return redirect('photo:detail', pk=photo.pk)


def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    print(comment)
    comment.delete()
    return redirect('photo:detail', pk=comment.photo.pk)
