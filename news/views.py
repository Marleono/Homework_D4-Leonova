from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.views import View
from .models import Post, Category
from .filters import PostFilter
from .forms import PostForm
from django.core.paginator import Paginator
from datetime import datetime

# class PostsList(ListView):
#     model = Post
#     template_name = 'posts.html'
#     context_object_name = 'posts'
#     queryset = Post.objects.order_by('-created')
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         return context
#
# class PostDetail(DetailView):
#     model = Post
#     template_name = 'post.html'
#     context_object_name = 'post'


# Create your views here.
class Posts(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    ordering = ['-created']
    paginate_by = 10



    def get_context_data(self, **kwargs): # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset()) # вписываем наш фильтр в контекст
        return context

class PostDetailView(DetailView):
    template_name = 'news_detail.html'
    queryset = Post.objects.all()

class PostCreateView(CreateView):
    template_name = 'news_add.html'
    form_class = PostForm


class PostUpdateView(UpdateView):
    template_name = 'news_add.html'
    form_class = PostForm

    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


# дженерик для удаления товара
class PostDeleteView(DeleteView):
    template_name = 'news_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'

class PostFilterView(View):
    template_name = 'news_search.html'
    form_class = PostForm

