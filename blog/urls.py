from django.urls import path


from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('category/<str:slug>/',
         views.CategoryListView.as_view(), name='category'),
    path('tags/<str:slug>/',
         views.TagsListView.as_view(), name='tags'),
    path('search/',
         views.SearchListView.as_view(), name='search'),
    path('post/<str:slug>/',
         views.singlePost.as_view(), name='single-post'),
]
