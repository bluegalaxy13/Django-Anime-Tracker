from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Anime

# Requests home webpage
def home(request):
    # Retrieve only the Anime objects associated with the logged-in user
    if request.user.is_authenticated:
        animes = Anime.objects.filter(user=request.user)
    else:
        animes = None

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "You Have Been Logged In!")
            return redirect('home')
        else:
            messages.success(request, "There Was An Error Logging In...")
            return redirect('home')
    else:
        return render(request, 'home.html', {'animes': animes})

# Logs out the user
def logout_user(request):
    logout(request)
    messages.success(request, "You Have Been Logged Out...")
    return redirect('home')

# Handles user registration
def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You Have Successfully Registered! Welcome!")
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})

# Displays a specific anime record
def anime_record(request, pk):
    if request.user.is_authenticated:
        anime_record = Anime.objects.get(id=pk, user=request.user)
        return render(request, 'record.html', {'anime_record': anime_record})
    else:
        messages.success(request, "You Must Be Logged In To View That Page...")
        return redirect('home')

# Deletes a specific anime record
def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Anime.objects.get(id=pk, user=request.user)
        delete_it.delete()
        messages.success(request, "Anime Deleted Successfully!")
        return redirect('home')
    else:
        messages.success(request, "You Must Be Logged In")
        return redirect('home')

# Adds a new anime record
def add_record(request):
    if request.user.is_authenticated:
        form = AddRecordForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                # Associate the new anime record with the logged-in user
                new_anime = form.save(commit=False)
                new_anime.user = request.user
                new_anime.save()
                messages.success(request, "Anime Successfully Added!")
                return redirect('home')
        return render(request, 'add_record.html', {'form': form})
    else:
        messages.success(request, "You Must Be Logged In...")
        return redirect('home')

# Updates an existing anime record
def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Anime.objects.get(id=pk, user=request.user)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Anime Record Has Been Updated!")
            return redirect('home')
        return render(request, 'update_record.html', {'form': form})
    else:
        messages.success(request, "You Must Be Logged In...")
        return redirect('home')
