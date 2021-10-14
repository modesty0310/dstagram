from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import PhotoList, PhotoCreate, PhotoDelete, PhotoDetail, PhotoUpdate, my_list
from . import views

# 다른앱들과 urlpatterns가 겹치는것을 방지 template에서 부를때 app_name:name로 부른다.
app_name = "photo"
urlpatterns = [  # path(경로, view, url pattern name)
    # class형 뷰는 as_view()를 붙여야함.
    path('create/', PhotoCreate.as_view(), name='create'),
    path('delete/<int:pk>/', PhotoDelete.as_view(), name="delete"),
    path('update/<int:pk>/', PhotoUpdate.as_view(), name='update'),
    path('detail/<int:pk>/', PhotoDetail.as_view(), name='detail'),
    path('', PhotoList.as_view(), name="index"),
    path('detail/<int:pk>/comment/', views.comment_write, name="comment_write"),
    path('detail/<int:pk>/comment_remove/',
         views.comment_remove, name="comment_remove"),
    path('<int:pk>/like/', views.like, name="like"),
    path('like/', views.like_list, name="like_list"),
    path('mylist/', views.my_list, name="my_list")
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
