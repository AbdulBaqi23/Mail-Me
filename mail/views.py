from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, ComposeForm
from .models import Email
from django.contrib.auth.models import User
from .encryption import encrypt_message, decrypt_message
from django.contrib import messages
from django.db.models import Q
from django.conf import settings

# create your views here.

def login_view(request):

    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            return redirect('inbox')
        else:
            messages.error(request, "Invalid credentials")
    return render(request, 'login.html')

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def inbox_view(request):
    query = request.GET.get('q')
    emails = Email.objects.filter(recipient=request.user)

    if query:
        # Filter encrypted messages after decrypting (you could also filter raw, but harder)
        filtered = []
        for email in emails:
            subject = decrypt_message(email.subject)
            body = decrypt_message(email.body_encrypted)
            if query.lower() in subject.lower() or query.lower() in body.lower():
                email.subject = subject
                email.body = body
                filtered.append(email)
        emails = filtered
    else:
        # Show all with decrypted fields
        for email in emails:
            email.subject = decrypt_message(email.subject)
            email.body = decrypt_message(email.body_encrypted)

    return render(request, 'inbox.html', {'emails': emails})

@login_required
def sent_view(request):
    query = request.GET.get('q')
    emails = Email.objects.filter(sender=request.user).order_by('-timestamp')

    if query:
        filtered = []
        for email in emails:
            subject = decrypt_message(email.subject)
            body = decrypt_message(email.body_encrypted)
            if query.lower() in subject.lower() or query.lower() in body.lower():
                email.subject = subject
                email.body = body
                filtered.append(email)
        emails = filtered
    else:
        for email in emails:
            email.subject = decrypt_message(email.subject)
            email.body = decrypt_message(email.body_encrypted)

    return render(request, 'sent.html', {'emails': emails})

@login_required
def compose_view(request):
    error = None
    if request.method == 'POST':
        form = ComposeForm(request.POST)
        if form.is_valid():
            recipient_username = form.cleaned_data['recipient']
            try:
                recipient = User.objects.get(username=recipient_username)
            except User.DoesNotExist:
                error = f"User '{recipient_username}' does not exist."
                return render(request, 'compose.html', {'form': form, 'error': error})

            subject_enc = encrypt_message(form.cleaned_data['subject'])
            encrypted_body = encrypt_message(form.cleaned_data['body'])
            Email.objects.create(
                sender=request.user,
                recipient=recipient,
                subject=subject_enc,
                body_encrypted=encrypted_body
            )
            return redirect('sent')
    else:
        form = ComposeForm()
    return render(request, 'compose.html', {'form': form, 'error': error})
