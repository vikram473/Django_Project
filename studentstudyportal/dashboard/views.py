from email.mime import audio
from multiprocessing import context
from re import search
from textwrap import shorten
from unittest import result
from urllib import request
from webbrowser import get
from django.shortcuts import render, redirect
import dashboard
from .forms import *
from .models import Notes
from django.contrib import messages
from django.views import generic
from .forms import HomeworkForm
from .models import Homework
from youtubesearchpython import VideosSearch
from .forms import TodoForm
from .models import Todo  
import requests
from .forms import DashboardForm
import wikipedia
from django.contrib.auth.decorators import login_required
# Home view
def home(request):
    return render(request, 'dashboard/home.html')

# Notes list and form submission
@login_required
def notes(request):
    if request.method == "POST":
        form = NotesForm(request.POST)
        if form.is_valid():
            notes = Notes(user=request.user, title=request.POST['title'], description=request.POST["description"])
            notes.save()
            messages.success(request, f"Notes Added from {request.user.username} Successfully")
    else:
        form = NotesForm()
    notes = Notes.objects.filter(user=request.user)
    context = {'notes': notes, 'form': form}
    return render(request, 'dashboard/notes.html', context)

# Note deletion
@login_required
def delete_note(request, pk=None):
    try:
        note = Notes.objects.get(id=pk)
        note.delete()
    except Notes.DoesNotExist:
        print(f"Note with id {pk} does not exist.")
    return redirect("notes")

# Notes detail view
class NotesDetailView(generic.DetailView):
    model = Notes

# Homework view 
@login_required
def homework(request):
    form = HomeworkForm()
    if request.method == 'POST':
        form = HomeworkForm(request.POST)
        if form.is_valid():
            homework = form.save(commit=False)
            homework.user = request.user
            homework.save()
            messages.success(request, "Homework Added Successfully!")
            return redirect('homework')  
    else:
        form = HomeworkForm()
    homeworks = Homework.objects.filter(user=request.user)
    homework_done = len(homeworks) == 0
    context = {
        'form': form,
        'homeworks': homeworks,
        'homework_done': homework_done,
    }
    return render(request, 'dashboard/homework.html', context)

@login_required
def update_homework(request,pk=None):
    homework = Homework.objects.get(id=pk)
    if homework.is_finished ==True:
        homework.is_finished = False
    else:
        homework.is_finished = True
    homework.save()
    return redirect('homework')

@login_required
def delete_homework(request,pk=None):
    Homework.objects.get(id=pk).delete()
    return redirect("homework")

# youtube view
def youtube(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST.get('text')
        result_list = []
        try:
            video = VideosSearch(text, limit=10)
            results = video.result().get('result', [])
            for i in results:
                result_dict = {
                    'input': text,
                    'title': i.get('title'),
                    'duration': i.get('duration'),
                    'thumbnail': i.get('thumbnails', [{}])[0].get('url'),
                    'channel': i.get('channel', {}).get('name'),
                    'link': i.get('link'),
                    'views': i.get('viewCount', {}).get('short'),
                    'published': i.get('publishedTime'),
                    'description': ''.join([j['text'] for j in i.get('descriptionSnippet', [])]) if i.get('descriptionSnippet') else 'No description'
                }
                result_list.append(result_dict)
        except Exception as e:
            print("YouTube search failed:", e)
            messages.error(request, "Error fetching YouTube videos. Try again later.")

        context = {
            'form': form,
            'results': result_list
        }
        return render(request, 'dashboard/youtube.html', context)
    else:
        form = DashboardForm()
    return render(request, 'dashboard/youtube.html', {'form': form})

# todo view
@login_required
def todo(request):
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            messages.success(request, "Todo added successfully!")
            return redirect('todo')  # redirect to the same page
    else:
        form = TodoForm()
    todos = Todo.objects.filter(user=request.user)
    todo_done = len(todos) == 0
    context = {
        'todos': todos,
        'form': form,
        'todo_done': todo_done,
    }
    return render(request, "dashboard/todo.html", context)

@login_required
def update_todo(request, pk):
    todo = Todo.objects.get(pk=pk)
    if todo.is_finished:
        todo.is_finished = False
    else:
        todo.is_finished = True
    todo.save()
    return redirect('todo')

@login_required
def delete_todo(request,pk=None):
    Todo.objects.get(id=pk).delete()
    return redirect("todo")

# books view 
def books(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            url = f"https://www.googleapis.com/books/v1/volumes?q={text}"
            r = requests.get(url)
            answer = r.json()
            result_list = []
            if 'items' in answer:
                for i in range(min(10, len(answer['items']))):
                    item = answer['items'][i].get('volumeInfo', {})
                    result_dict = {
                        'title': item.get('title'),
                        'subtitle': item.get('subtitle'),
                        'description': item.get('description'),
                        'count': item.get('pageCount'),
                        'categories': item.get('categories'),
                        'rating': item.get('averageRating'),
                        'thumbnail': item.get('imageLinks', {}).get('thumbnail'),
                        'preview': item.get('previewLink'),
                    }
                    result_list.append(result_dict)

            context = {
                'form': form,
                'results': result_list
            }
            return render(request, 'dashboard/books.html', context)
    else:
        form = DashboardForm()

    return render(request, 'dashboard/books.html', {'form': form})

# dictionary view
def dictionary(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{text}"
            r = requests.get(url)
            answer = r.json()
            try:
                phonetics = answer[0]['phonetics'][0].get('text', '')
                audio = answer[0]['phonetics'][0].get('audio', '')
                definition = answer[0]['meanings'][0]['definitions'][0].get('definition', 'No definition available.')
                example = answer[0]['meanings'][0]['definitions'][0].get('example', 'No example available.')
                context = {
                    'form': form,
                    'input': text,
                    'phonetics': phonetics,
                    'audio': audio,
                    'definition': definition,
                    'example': example,
                }
            except (IndexError, KeyError, TypeError):
                context = {
                    'form': form,
                    'input': text,
                    'error': "Could not fetch results. Try a different word or check API limit."
                }
            return render(request, "dashboard/dictionary.html", context)
    else:
        form = DashboardForm()
    return render(request, 'dashboard/dictionary.html', {'form': form})

# Wikipedia view
def wiki(request): 
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            try:
                search = wikipedia.page(text)
                context = {
                    'form': form,
                    'title': search.title,
                    'link': search.url,
                    'details': search.summary,
                }
            except wikipedia.exceptions.DisambiguationError as e:
                context = {
                    'form': form,
                    'error': f"Too many results. Try one of these: {', '.join(e.options[:5])}"
                }
            except wikipedia.exceptions.PageError:
                context = {
                    'form': form,
                    'error': "Page not found. Try a different word."
                }
            return render(request, "dashboard/wiki.html", context)
    else:
        form = DashboardForm()

    return render(request, 'dashboard/wiki.html', {'form': form})

# conversion view
def conversion(request):
    if request.method == "POST":
        form = ConversionForm(request.POST)
        measurement_type = request.POST.get('measurement')

        if measurement_type == 'length':
            measurement_form = ConversionForm(request.POST)
            context = {
                'form': form,
                'm_form': measurement_form,
                'input': True,
            }
            if 'input' in request.POST:
                first = request.POST.get('measure1')
                second = request.POST.get('measure2')
                input_value = request.POST.get('input')
                answer = ''
                if input_value and float(input_value) >= 0:
                    if first == 'yard' and second == 'foot':
                        answer = f'{input_value} yard = {float(input_value) * 3:.2f} foot'
                    elif first == 'foot' and second == 'yard':
                        answer = f'{input_value} foot = {float(input_value) / 3:.2f} yard'
                context['answer'] = answer

        elif measurement_type == 'mass':
            measurement_form = ConversionMassForm(request.POST)
            context = {
                'form': form,
                'm_form': measurement_form,
                'input': True,
            }
            if 'input' in request.POST:
                first = request.POST.get('measure1')
                second = request.POST.get('measure2')
                input_value = request.POST.get('input')
                answer = ''
                if input_value and float(input_value) >= 0:
                    if first == 'pound' and second == 'kilogram':
                        answer = f'{input_value} pound = {float(input_value) * 0.453592:.2f} kilogram'
                    elif first == 'kilogram' and second == 'pound':
                        answer = f'{input_value} kilogram = {float(input_value) * 2.20462:.2f} pound'
                context['answer'] = answer

        else:
            context = {'form': form, 'input': False}

    else:
        form = ConversionForm()
        context = {
            'form': form,
            'input': False
        }

    return render(request, "dashboard/conversion.html", context)

# Registration view
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f"Account Created for {username}!!")
            return redirect("login")
    else:
        form = UserRegistrationForm()
    context = {
        'form':form,
    }
    return render(request,"dashboard/register.html",context)
    
# profile view
@login_required
def profile(request):
    homeworks = Homework.objects.filter(is_finished = False,user =request.user )
    todos = Todo.objects.filter(is_finished = False,user =request.user )
    if len(homeworks) == 0:
        homework_done = True
    else:
        homework_done = False
    if len(todos) == 0:
        todos_done = True
    else:
        todos_done = False
    context = {
        'homework': homeworks,
        'todos':todos,
        'homework_done': homework_done,
        'todos_done': todos_done,
    }  
    return render(request,"dashboard/profile.html", context)
