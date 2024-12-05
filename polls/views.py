# polls/views.py
from django.forms import formset_factory
from django.shortcuts import render, get_object_or_404, redirect
from .models import Poll, Choice
from .forms import PollForm, ChoiceFormSet, CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


# Home page with polls

def logout_view(request):
    logout(request)
    return redirect('polls:login')

@login_required
def index(request):
    polls = Poll.objects.filter(created_by=request.user) 
    return render(request, 'polls/index.html', {'polls': polls})


@login_required
def poll_detail(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id, created_by=request.user)  
    return render(request, 'polls/poll_detail.html', {'poll': poll})


@login_required
def vote(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id, created_by=request.user) 
    try:
        selected_choice = poll.choices.get(id=request.POST['choice'])
        selected_choice.votes += 1
        selected_choice.save()
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/poll_detail.html', {
            'poll': poll,
            'error_message': "You didn't select a choice.",
        })
    return redirect('polls:results', poll_id=poll.id)


@login_required
def create_poll(request):
    num_choices = request.GET.get('num_choices', 2)  
    try:
        num_choices = int(num_choices)
    except ValueError:
        num_choices = 2

    DynamicChoiceFormSet = formset_factory(
        ChoiceFormSet.form,
        extra=num_choices,
        can_delete=True
    )

    if request.method == 'POST':
        poll_form = PollForm(request.POST)
        formset = DynamicChoiceFormSet(request.POST)
        if poll_form.is_valid() and formset.is_valid():
            poll = poll_form.save(commit=False)
            poll.created_by = request.user  
            poll.save()
            for form in formset:
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    choice = form.save(commit=False)
                    choice.poll = poll
                    choice.save()
            return redirect('polls:index')
    else:
        poll_form = PollForm()
        formset = DynamicChoiceFormSet()

    return render(request, 'polls/create_poll.html', {
        'poll_form': poll_form,
        'formset': formset,
        'num_choices': num_choices,
    })


@login_required
def edit_poll(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id, created_by=request.user) 
    if request.method == 'POST':
        poll_form = PollForm(request.POST, instance=poll)
        formset = ChoiceFormSet(request.POST, instance=poll)
        
        if poll_form.is_valid() and formset.is_valid():
            poll_form.save()
            formset.save()
            return redirect('polls:index')
    else:
        poll_form = PollForm(instance=poll)
        formset = ChoiceFormSet(instance=poll)
    
    return render(request, 'polls/edit_poll.html', {'poll_form': poll_form, 'formset': formset})


@login_required
def delete_poll(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id, created_by=request.user)  
    if request.method == 'POST':
        poll.delete()
        return redirect('polls:index')
    return render(request, 'polls/delete_poll.html', {'poll': poll})


@login_required
def poll_results(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id, created_by=request.user)  
    return render(request, 'polls/results.html', {'poll': poll})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('polls:index')  
        form = AuthenticationForm()
    return render(request, 'polls/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('polls:login') 
    else:
        form = CustomUserCreationForm()
    return render(request, 'polls/register.html', {'form': form})
