from django.shortcuts import get_object_or_404, redirect, render
from .models import *
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from .forms import PostForm, CommentForm

# Create your views here.
class PostViewList(ListView):
    model = Post


class PostViewCreate(CreateView):
    form_class = PostForm
    model = Post
    success_url = "/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "view_type": "create"
        })

        return context

class PostViewUpdate(UpdateView):
    form_class = PostForm
    model = Post
    success_url = "/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "view_type": "update"
        })

        return context


class PostViewDetail(DetailView):
    model = Post

    def get_object(self, **kwargs):
        object = super().get_object(**kwargs)
        PostView.objects.get_or_create(user=self.request.user, post=object)

        return object

    def post(self, *args, **kwargs):
        form = CommentForm(self.request.POST)
        if form.is_valid():
            post = self.get_object()
            comment = form.instance
            comment.user = self.request.user
            comment.post = post
            comment.save()
            return redirect("details", slug=post.slug)

        return redirect("details", slug=self.get_object().slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'form':CommentForm()
        })

        return context



class PostViewDelete(DeleteView):
    model = Post
    success_url = "/"
    


def like(request, slug):
    post = get_object_or_404(Post, slug=slug)
    like_qs = Like.objects.filter(user=request.user, post=post)
    if like_qs.exists():
        like_qs[0].delete()
        return redirect("details", slug=slug)
    Like.objects.create(user=request.user, post=post)
    return redirect("details", slug=slug)

