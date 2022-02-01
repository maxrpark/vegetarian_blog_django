from django.shortcuts import get_object_or_404, render
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q
from django.views.generic import ListView

from .models import Article, Category, Tags
from .form import commentForm


class HomeView(View):
    def get(self, request):
        all_post = Article.objects.all()
        restaurant_posts = all_post.filter(
            category__slug='cafes-y-restaurantes').order_by("-id",)
        snacks_posts = all_post.filter(category__slug='snack').order_by("-id",)
        new_post = all_post.last
        Latests_post = all_post.order_by("-id",)

        context = {
            "new_post": new_post,
            "Latests_post": Latests_post[1:4],
            "snacks_posts": snacks_posts[0:3],
            "restaurant_posts": restaurant_posts[0:3]
        }
        return render(request, 'blog/index.html', context)


class CategoryListView(View):
    def get(self, request, slug):
        all_post = Article.objects.all()
        posts = all_post.filter(category__slug=slug)
        all_categories = Category.objects.all()
        category = all_categories.get(slug=slug)

        all_post = Article.objects.all()

        latests_post = all_post.order_by("-id",)
        context = {
            "posts": posts,
            "category": category,
            "latests_post": latests_post[0:4],
            "categories": all_categories,
        }
        return render(request, 'blog/category_page.html', context)


class TagsListView(View):
    def get(self, request, slug):
        all_post = Article.objects.all()
        posts = all_post.filter(tags__slug=slug)
        tags = Tags.objects.filter(slug=slug).last

        all_categories = Category.objects.all()
        latests_post = all_post.order_by("-id",)[0:4]
        context = {
            "posts": posts,
            "tag": tags,
            "latests_post": latests_post,
            "categories": all_categories,
        }
        return render(request, 'blog/tags_page.html', context)


class singlePost(View):
    def get(self, request, slug):
        post = get_object_or_404(Article, slug=slug)
        post_category = post.category.slug
        all_post = Article.objects.all()
        related_posts = all_post.filter(category__slug=post_category)
        all_categories = Category.objects.all()
        latests_post = all_post.order_by("-id",)[0:4]
        context = {
            "post": post,
            "latests_post": latests_post,
            "categories": all_categories,
            "related_posts": related_posts[0:3],
            "tags": post.tags.all(),
            "comments_form": commentForm(),
            "comments": post.comments.all().order_by('-id')
        }
        return render(request, 'blog/single_post.html', context)

    def post(self, request, slug):
        comment_form = commentForm(request.POST)
        post = get_object_or_404(Article, slug=slug)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.article = post
            comment.save()
            return HttpResponseRedirect(reverse('single-post', args=[slug]))

        context = {
            "post": post,
            "tags": post.tags.all(),
            "comments_form": comment_form,
            "comments": post.comments.all().order_by('-id')
        }
        return render(request, 'blog/single_post.html', context)


class SearchListView(View):
    def get(self, request):
        query = request.GET.get('query', '')

        all_post = Article.objects.all()
        posts = posts = Article.objects.filter(status=Article.ACTIVE).filter(
            Q(title__icontains=query) | Q(description__icontains=query) | Q(body__icontains=query))
        all_categories = Category.objects.all()
        latests_post = all_post.order_by("-id",)[0:4]

        context = {
            "query": query,
            "posts": posts,
            "latests_post": latests_post,
            "categories": all_categories,
        }

        return render(request, "blog/search_page.html", context)
