from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify


class Author(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    description = models.TextField()

    def __str__(self):
        return self.first_name


class Tags(models.Model):
    tag = models.CharField(max_length=50)
    slug = models.SlugField(max_length=150, unique=True, null=True)

    class Meta:
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.tag


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    slug = models.SlugField(max_length=150, unique=True, null=True)

    def __str__(self):
        return self.name


class Article(models.Model):
    ACTIVE = 'active'
    DRAFT = 'draft'

    CHOICES_STATUS = (
        (ACTIVE, 'Active'),
        (DRAFT, 'Draft')
    )

    title = models.CharField(max_length=200)
    description = models.TextField(max_length=200)
    # image = models.ImageField(
    #     upload_to="uploads/",
    #     max_length=100,
    #     blank=True,
    #     null=True,)
    image = models.ImageField(upload_to='vegetarianBlog/', null=True)
    body = RichTextField()
    author = models.ForeignKey(
        Author, related_name="article", on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category, related_name="article", on_delete=models.CASCADE)
    status = models.CharField(
        max_length=10, choices=CHOICES_STATUS, default=ACTIVE)
    tags = models.ManyToManyField(Tags, related_name="article")
    date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=150, unique=True, editable=True)

    def __str__(self):
        return self.title

    def get_image(self):
        if self.image:
            return 'http://127.0.0.1:8000' + self.image.url
        return ''

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Article, self).save(*args, **kwargs)


class Comments(models.Model):
    article = models.ForeignKey(
        Article, related_name='comments', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=150)
    title = models.CharField(max_length=150)
    messege = models.TextField()

    class Meta:
        verbose_name_plural = 'Comments'

    def __str__(self):
        return self.name
