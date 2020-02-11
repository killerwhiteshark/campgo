from django.shortcuts import render, redirect
from .models import Campsite, Comment
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CommentForm


def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

@login_required
def index(request):
  campsites = Campsite.objects.all()
  return render(request, 'campgo/index.html', { 'campsites': campsites })

class CampsiteCreate(LoginRequiredMixin, CreateView):
  model = Campsite
  fields = ['name', 'location', 'img_url', 'description']
  def form_valid(self, form):
    form.instance.owner = self.request.user
    return super().form_valid(form)

@login_required
def camp_show(request, campsite_id):
  campsite = Campsite.objects.get(id=campsite_id)
  comment_form = CommentForm()
  return render(request, 'campgo/show.html', { 
    'campsite': campsite,
    'comment_form': comment_form
    })

class CampsiteUpdate(LoginRequiredMixin, UpdateView):
  model = Campsite
  fields = ['name', 'location', 'img_url', 'description']
  success_url="/camp_show/{campsite_id}/"

@login_required
def camp_delete(request):
  return render(request, 'campgo/confirm.html')

@login_required
def add_comment(request, campsite_id):
  form = CommentForm(request.POST)
  if form.is_valid():
    new_comment = form.save(commit=False)
    new_comment.campsite_id = campsite_id
    form.instance.user = request.user
    new_comment.save()
  return redirect('camp_show', campsite_id = campsite_id)

# comment views
# @login_required
# def assoc_comments(request, campsite_id, comment_id):
#   Campsite.objects.get(id=campsite_id).comments.add(comment_id)
#   return redirect('detail', campsite_id=campsite_id)

# @login_required
# def unassoc_comments(request, campsite_id, comment_id):
#   Campsite.objects.get(id=campsite_id).comments.remove(comment_id)
#    return redirect('detail', campsite_id=campsite_id)

class CommentUpdate(LoginRequiredMixin, UpdateView):
  model = Comment
  fields = ['content']

class CommentDelete(LoginRequiredMixin, DeleteView):
  model = Comment
  success_url="/camp_show/{campsite_id}/"

@login_required
def add_fav(request, campsite_id):
  user = request.user
  Campsite.objects.get(id=campsite_id).users.add(user)
  return redirect('camp_show', campsite_id=campsite_id)

@login_required
def fav_list(request, user_id):
  user = request.user
  user = request.user
  campsite = Campsite.objects.get(id=campsite_id)
  user.campsite_set.add(campsite)
  success_url="/camp_show/{campsite_id}/"

@login_required
def fav_list(request, user_id):
  user = request.user
  campsites = user.campsite_set.all()
  return render(
    request,
    'main_app/favlist.html',
    { 'campsites': campsites }
  )
=======
# @login_required
# def add_fav(request, campsite_id):
#   user = request.user
#   campsite = Campsite.objects.get(id=campsite_id)
#   user.campsite_set.add(campsite)

# @login_required
# def add_fav(request, campsite_id):
#   success_url="/camp_show/{campsite_id}/"

# @login_required
# def fav_list(request, user_id):
#   user = request.user
#   campsites = user.campsite_set.all()
#   return render(
#     request,
#     'campgo/main_app/favlist.html',
#     { 'campsites': campsites }
#   )

@login_required
def fav_list(request, user_id):
  return render(request, 'campgo/favlist.html')

@login_required
def assoc_favlist(request, user_id, campsite_id):
  Campsite.objects.get(id=campsite_id).favlist.add(user_id)
  return redirect('favlist', user_id=user_id)

@login_required
def unassoc_favlist(request, user_id, campsite_id):
  Campsite.objects.get(id=campsite_id).favlist.remove(user_id)
  return redirect('favlist', user_id=user_id)

@login_required
def search_new(request):
  return render(request, 'campgo/search_new.html')

#   user = request.user
#   campsites = user.campsite_set.all()
#   return render(
#     request,
#     'main_app/favlist.html',
#     { 'campsites': campsites }
#   )
