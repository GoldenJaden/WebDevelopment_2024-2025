from django.shortcuts import render
from .forms import ContactForm
from .models import ContactMessage

def home_view(request):
    latest_messages = ContactMessage.objects.order_by('-created_at')[:5]
    return render(request, 'mainapp/home.html', {'latest_messages': latest_messages})


def about_view(request):
    return render(request, 'mainapp/about.html')

def contact_view(request):
    sent = False
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            ContactMessage.objects.create(**form.cleaned_data)
            sent = True
    else:
        form = ContactForm()
    return render(request, 'mainapp/contact.html', {'form': form, 'sent': sent})

def messages_view(request):
    messages = ContactMessage.objects.all().order_by('-created_at')
    return render(request, 'mainapp/messages.html', {'messages': messages})
