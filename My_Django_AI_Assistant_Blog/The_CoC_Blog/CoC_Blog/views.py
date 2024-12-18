from django.shortcuts import render, get_object_or_404
from django.views.generic import (ListView,
                                  DetailView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView
                                  )
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        UserPassesTestMixin
                                        )
from django.contrib.auth.models import User
from .models import Post


import re
import json
import ollama
from ollama import Client


ollama_url = 'http://localhost:11434'





def home(request):
    context = {
        'posts' : Post.objects.all()
        }    
    return render(request, 'CoC_Blog/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'CoC_Blog/home.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 3


class UserPostListView(ListView):
    model = Post
    template_name = 'CoC_Blog/user_posts.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

                                   
class PostDetailView(DetailView):
    model = Post



class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)



class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
  

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    
def about(request):
    return render(request, 'CoC_Blog/about.html', {'title': about})


def ai_assistant(request):
    if request.method == 'POST':
        user_query = request.POST.get('query')
        ai_response = tinyllama_ai(user_query)
        return render(request, 'ai_assistant.html', {'response': ai_response})
    return render(request, 'ai_assistant.html')

def tinyllama_ai(query):
    headers = {"Authorization": "Bearer YOUR_OLLAMA_API_KEY"}

    My_GPT_response = ollama.chat(
        model='tinyllama',
        messages=[{'role': 'user', 'content': query},],
        stream=False,
    )

    response_GPT = My_GPT_response['message']['content']    
    print("response_GPT : ", response_GPT)

    New_Edited_GPT_Response = response_GPT
    print("New_Edited_GPT_Response : ", New_Edited_GPT_Response)
    
    payload = New_Edited_GPT_Response
    response = New_Edited_GPT_Response

    return response



