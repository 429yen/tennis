from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('groups', views.groups, name='groups'),
    path('add', views.add, name='add'),
    path('creategroup', views.creategroup, name='creategroup'),
    path('post', views.post, name='post'),
    path('messagedelete/<int:message_id>', views.messagedelete, name='messagedelete' ),
    path('good/<int:good_id>', views.good, name='good'),
    path('gooddetail/<int:message_id>', views.gooddetail, name='gooddetail'),
    path('goodadd/<int:message_id>', views.goodadd, name='goodadd'),
    path('gooddelete/<int:message_id>/<int:good_id>', views.gooddelete, name='gooddelete'),
    path('goodedit/<int:message_id>/<int:good_id>', views.goodadd, name='goodedit'),
    path('myproducts', views.myproducts, name='myproducts')
]