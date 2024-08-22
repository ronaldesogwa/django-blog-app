from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from .models import Post
#new
from django.views.generic.edit import FormMixin
from .forms import CommentForm

# Create your views here.

class BlogListView(ListView):
    model = Post
    template_name = 'home.html'

class ProfileBlogListView(LoginRequiredMixin,ListView):
    model = Post
    template_name = 'profile.html'

    def get_queryset(self):
        all_posts = Post.objects.all()
        filtered_posts = Post.objects.filter(author=self.request.user)
        return filtered_posts

class BlogDetailView(FormMixin,DetailView):
    model = Post
    template_name = 'post_detail.html'
    form_class = CommentForm

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk':self.object.pk} )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all
        if 'form' not in context:
            context['form'] = self.get_form()
        return context
    
    def post(self, request, *args, **kwargs):
        self.object =self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        
    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.post = self.object
        comment.author = self.request.user
        comment.save()
        return super().form_valid(form)
    

class BlogCreateView(LoginRequiredMixin,CreateView):
    model = Post
    template_name = 'new_post.html'
    fields = ['title', 'author', 'body']

class BlogUpdateView(LoginRequiredMixin,UpdateView):
    model = Post
    template_name = "post_edit.html"
    fields = ['title', 'body']

class BlogDeleteView(LoginRequiredMixin,DeleteView):
    model = Post
    template_name = "post_delete.html"
    success_url = reverse_lazy('home')