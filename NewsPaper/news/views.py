from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Post
from .forms import PostForm


class NewsListView(ListView):
    model = Post
    template_name = "news/news_list.html"
    context_object_name = "news_list"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context["paginator"]
        page = context["page_obj"]

        index = page.number - 1
        max_index = paginator.num_pages

        start_index = max(index - 2, 0)
        end_index = min(index + 3, max_index)

        page_range = list(paginator.page_range)[start_index:end_index]
        context["page_range"] = page_range
        return context


class NewsSearchView(ListView):
    model = Post
    template_name = "news/news_search.html"
    context_object_name = "news_list"
    paginate_by = 10

    def get_queryset(self):
        queryset = Post.objects.all()
        title = self.request.GET.get("title", "")
        author = self.request.GET.get("author", "")
        date_after = self.request.GET.get("date_after", "")

        if title:
            queryset = queryset.filter(title__icontains=title)
        if author:
            queryset = queryset.filter(author__user__username__icontains=author)
        if date_after:
            queryset = queryset.filter(created_at__gte=date_after)

        return queryset



class NewsCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "news/news_form.html"
    success_url = reverse_lazy("news_list")
    permission_required = "news.add_post"



class NewsUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "news/news_form.html"
    success_url = reverse_lazy("news_list")
    permission_required = "news.change_post"



class NewsDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = "news/news_confirm_delete.html"
    success_url = reverse_lazy("news_list")
    permission_required = "news.delete_post"

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import redirect

@login_required
def become_author(request):
    author_group = Group.objects.get(name="authors")
    request.user.groups.add(author_group)
    return redirect("profile")

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import CreateView
from .models import Post

class PostCreateView(PermissionRequiredMixin, CreateView):
    model = Post
    fields = ["title", "content"]
    permission_required = "news.add_post"
    template_name = "post_form.html"
