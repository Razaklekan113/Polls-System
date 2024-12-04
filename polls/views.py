from django.shortcuts import render, get_object_or_404, redirect
from .models import Poll, Choice
from .forms import PollForm, ChoiceFormSet
from django.forms import formset_factory

def index(request):
    polls = Poll.objects.all()
    return render(request, 'polls/index.html', {'polls': polls})

def poll_detail(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    return render(request, 'polls/poll_detail.html', {'poll': poll})

def vote(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
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

def create_poll(request):
    # Handle number of choices dynamically
    num_choices = request.GET.get('num_choices', 2)  # Default to 2 choices
    try:
        num_choices = int(num_choices)
    except ValueError:
        num_choices = 2

    # Create a dynamic formset factory with the desired number of extra forms
    DynamicChoiceFormSet = formset_factory(
        ChoiceFormSet.form,
        extra=num_choices,
        can_delete=True
    )

    if request.method == 'POST':
        poll_form = PollForm(request.POST)
        formset = DynamicChoiceFormSet(request.POST)
        if poll_form.is_valid() and formset.is_valid():
            poll = poll_form.save()
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

def edit_poll(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    
    # Handle the POST request
    if request.method == 'POST':
        poll_form = PollForm(request.POST, instance=poll)
        formset = ChoiceFormSet(request.POST, instance=poll)
        
        # Check if both the poll form and formset are valid
        if poll_form.is_valid() and formset.is_valid():
            poll_form.save()  # Save the poll form
            formset.save()  # Save the formset with choices
            return redirect('polls:index')  # Redirect to polls list after saving
    else:
        # If it's a GET request, use the existing data in the form
        poll_form = PollForm(instance=poll)
        formset = ChoiceFormSet(instance=poll)
    
    # Render the edit poll template with forms
    return render(request, 'polls/edit_poll.html', {'poll_form': poll_form, 'formset': formset})

def delete_poll(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    if request.method == 'POST':
        poll.delete()
        return redirect('polls:index')
    return render(request, 'polls/delete_poll.html', {'poll': poll})

def results(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    return render(request, 'polls/results.html', {'poll': poll})

