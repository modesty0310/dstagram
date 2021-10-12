from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import PhotoList, PhotoCreate, PhotoDelete, PhotoDetail, PhotoUpdate

app_name = "photo"  # 다른앱들과 urlpatterns가 겹치는것을 방지
urlpatterns = [  # path(경로, view, url pattern name)
    # class형 뷰는 as_view()를 붙여야함.
    path('create/', PhotoCreate.as_view(), name='create'),
    path('delete/<int:pk>', PhotoDelete.as_view(), name="delete"),
    path('update/<int:pk>', PhotoUpdate.as_view(), name='update'),
    path('detail/<int:pk>', PhotoDetail.as_view(), name='detail'),
    path('', PhotoList.as_view(), name="index")
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
