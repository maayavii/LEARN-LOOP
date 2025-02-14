# support/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import SupportTicket
from .forms import SupportTicketForm

# Remove @login_required if user is already authenticated in your main app
def create_ticket(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Replace 'login' with your login URL name
        
    if request.method == 'POST':
        form = SupportTicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            messages.success(request, 'Your support ticket has been submitted successfully.')
            return redirect('support:ticket_list')
    else:
        form = SupportTicketForm()
    return render(request, 'support/create_ticket.html', {'form': form})

# Similarly for ticket list view
def ticket_list(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Replace 'login' with your login URL name
        
    if not request.user.is_superuser:
        tickets = SupportTicket.objects.filter(user=request.user).order_by('-created_at')
    else:
        tickets = SupportTicket.objects.all().order_by('-created_at')
    return render(request, 'support/ticket_list.html', {'tickets': tickets})