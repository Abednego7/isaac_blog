# from datetime import date
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Post

# all_posts = []

"""
def get_date(post):
    return post["date"]  # key -> post dictionary
"""


# Create your views here.
# Como clase (antes solo era la funcion: starting_page):
class StartingPageView(ListView):
    template_name = "blog/index.html"
    model = Post
    # Ordering permite una lista con mas campos ejm: ["-date", "name"]
    ordering = ["-date"]
    context_object_name = "posts"

    # Controla como se consultaran los datos
    def get_queryset(self):
        # toda la data
        queryset = super().get_queryset()
        data = queryset[:3]
        return data


"""
# Como funcion:
def starting_page(request):

    # sorted_posts = sorted(all_posts, key=get_date)
    # latest_posts = sorted_posts[-3:]

    # Nota: Django no acepta indexacion engativa
    # - : Decendente
    latest_posts = Post.objects.all().order_by("-date")[:3]
    return render(request, "blog/index.html", {"posts": latest_posts})
"""


# Como clase (antes solo era la funcion: posts):
class AllPostsView(ListView):
    template_name = "blog/all-posts.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "all_posts"


"""
def posts(request):
    all_posts = Post.objects.all().order_by("-date")
    return render(request, "blog/all-posts.html", {"all_posts": all_posts})
"""


# Como clase (antes solo era la funcion: post_detail):
# DetailView viene con todo preparado para los slug y los errores 404
class SinglePostView(DetailView):
    template_name = "blog/post-detail.html"
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post_tags"] = self.object.tag.all()
        return context


"""
def post_detail(request, slug):
    # identified_post = next(post for post in all_posts if post["slug"] == slug)
    identified_post = get_object_or_404(Post, slug=slug)
    return render(
        request,
        "blog/post-detail.html",
        {"post": identified_post, "post_tags": identified_post.tag.all()},
    )
"""
