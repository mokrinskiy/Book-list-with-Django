from typing import Any, Optional
from django.db import models
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View, TemplateView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login
from django.db.models import Count
from .models import *
from .forms import *

class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Home'
        return context
    

class BookListView(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'book_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        statuses = ['To read', 'Reading', 'Read', 'Postponed', 'Abandoned']
        book_list = {}
        books_count = 0
        for status in statuses:
            book_list[status] = Book.objects.filter(owner=self.request.user, status=status)
        for key, value in book_list.items():
            books_count += len(value)
        context["book_list"] = book_list
        context["books_count"] = books_count
        context["title"] = 'Book list'
        return context
    
    def get_queryset(self):
        return Book.objects.filter(owner=self.request.user)
    

class BookDetailView(DetailView):
    model = Book
    context_object_name = 'book'
    template_name = 'book_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'About book'
        return context
    

class BookCreateView(LoginRequiredMixin, CreateView):
    model = Book
    form_class = BookCreateForm
    success_url = reverse_lazy('book_list')
    template_name = 'book_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Adding a book'
        return context
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
    

class BookUpdateView(UpdateView):
    model = Book
    form_class = BookUpdateForm
    success_url = reverse_lazy('book_list')
    template_name = 'book_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Edit a book'
        return context
    

class BookDeleteView(DeleteView):
    model = Book
    success_url = reverse_lazy('book_list')
    template_name = 'book_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Deleting a book'
        return context
    

class RegisterUser(CreateView):
    form_class = SignUpForm
    template_name = 'register.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Registration'
        return context
    
    def form_valid(self, form) -> HttpResponse:
        user = form.save()
        login(self.request, user)
        return redirect('book_list')
    

class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = "login.html"
    http_method_names = ['get', 'post']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Login'
        return context
    
    def get_success_url(self):
        return reverse_lazy('book_list')


def logout_user(request):
    logout(request)
    return redirect('login')


class UserProfileView(DetailView):
    model = User
    context_object_name = 'profile_user'
    template_name = 'user_profile.html'

    def get_object(self, queryset=None):
        username = self.kwargs['username']
        user = User.objects.get(username=username)
        return user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        statuses = ['Read', 'Reading', 'To read', 'Postponed', 'Abandoned']
        book_counts = {}
        for status in statuses:
            book_counts[status] = Book.objects.filter(owner=self.request.user, status=status).count()
        context["book_counts"] = book_counts
        context["total_books_added"] = sum(book_counts.values())
        context["title"] = f"Profile {self.request.user}"
        return context
    

class AuthorAddView(CreateView):
    model = Author
    form_class = AuthorAddForm
    success_url = reverse_lazy('book_create')
    template_name = 'add_author.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Adding author"
        return context
    
    
def support(request):
    if request.method == 'POST':
        form = SupportMessageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('support_thanks')
    else:
        form = SupportMessageForm()
    return render(request, 'support.html', {'form': form, 'title': 'Support'})


class SupportThanks(TemplateView):
    template_name = 'support_thanks.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Thanks"
        return context
    