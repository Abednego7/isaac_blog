# from datetime import date
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.views import View
from .models import Post
from .forms import CommentForm

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
class SinglePostView(View):
    def is_stored_post(self, request, post_id):
        stored_posts = request.session.get("stored_posts")

        if stored_posts is not None:
            is_saved_for_later = post_id in stored_posts
        else:
            is_saved_for_later = False

        return is_saved_for_later

    def get(self, request, slug):
        post = Post.objects.get(slug=slug)

        # Ahi iba todo el contenido de la funcion creada de is_stored_post
        # se creo una funcion para no repetir codigo

        context = {
            "post": post,
            "post_tags": post.tag.all(),
            "comment_form": CommentForm(),
            # related_name -> comments
            "comments": post.comments.all().order_by("-id"),
            "saved_for_later": self.is_stored_post(request, post.id),
        }
        return render(request, "blog/post-detail.html", context)

    def post(self, request, slug):
        comment_form = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)

        if comment_form.is_valid():
            # al hacer esto (commit=false), la llamada a guardar, no afectara a la bd;
            # sino que creara una nueva instancia del modelo (en nuestro caso: un nuevo comentario):
            comment = comment_form.save(commit=False)  # entrada del usuario en el form
            comment.post = post  # datos adicionales agregados por nosotros para el fk
            comment.save()
            # reverse nos permite crear urls automaticas usando los nombres de las urls
            return HttpResponseRedirect(reverse("post-detail-page", args=[slug]))

        context = {
            "post": post,
            "post_tags": post.tag.all(),
            "comment_form": comment_form,
            # related_name -> comments
            "comments": post.comments.all().order_by("-id"),
            "saved_for_later": self.is_stored_post(request, post.id),
        }
        return render(request, "blog/post-detail.html", context)


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


class ReadLaterView(View):
    def get(self, request):
        stored_posts = request.session.get("stored_posts")
        context = {}

        if stored_posts is None or len(stored_posts) == 0:
            context["posts"] = []
            context["has_posts"] = False
        else:
            # __in -> filtra los resultados dependiendo de una lista
            posts = Post.objects.filter(id__in=stored_posts)
            context["posts"] = posts
            context["has_posts"] = True

        return render(request, "blog/stored-posts.html", context)

    def post(self, request):
        stored_posts = request.session.get("stored_posts")

        if stored_posts is None:
            stored_posts = []

        post_id = int(request.POST["post_id"])

        if post_id not in stored_posts:
            stored_posts.append(post_id)
        else:
            stored_posts.remove(post_id)

        request.session["stored_posts"] = stored_posts

        return HttpResponseRedirect("/")
