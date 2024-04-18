from django.urls import path
from django.views.decorators.cache import cache_page

from blog.apps import BlogConfig
from blog.views import BlogListView, BlogCreateView, BlogUpdateView, BlogDetailView, BlogDeleteView

app_name = BlogConfig.name

urlpatterns = [
    path('', BlogListView.as_view(), name='blog_list'),
    path('blog/create/', BlogCreateView.as_view(), name='blog_create'),
    path('blog/edit/<str:slug>/', BlogUpdateView.as_view(), name='blog_update'),
    path('blog/<str:slug>/', cache_page(10)(BlogDetailView.as_view()), name='blog_detail'),
    path('blog/delete/<str:slug>/', cache_page(60)(BlogDeleteView.as_view()), name='blog_delete'),
]