from django.urls import path

from .views import (
    PostList, CategoryList, ProfileView,
    ProfileUpdate, PostDetail, ProfileDelete,
    ResponseList, ResponseAcceptView, PostCreate,
    logout_user
)


urlpatterns = [
    path('', PostList.as_view(), name='posts'),
    path('category/<int:category_id>/', CategoryList.as_view(), name='category'),
    path('post/<int:pk>/', PostDetail.as_view(), name='post'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    path('profile/<int:pk>/edit', ProfileUpdate.as_view(), name='profile_edit'),
    path('profile/<int:pk>/delete', ProfileDelete.as_view(), name='profile_delete'),
    path('responses/', ResponseList.as_view(), name='responses'),
    path('post/<int:pk>/response/<int:response_pk>/', ResponseAcceptView.as_view(), name='response'),
    path('post/edit/', PostCreate.as_view(), name='create_post'),
    path('logout/', logout_user, name='logout'),

]