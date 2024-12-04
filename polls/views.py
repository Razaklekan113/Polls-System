from django.shortcuts import render, get_object_or_404, redirect
from .models import Poll, Choice
from .forms import PollForm, ChoiceFormSet

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
    if request.method == 'POST':
        poll_form = PollForm(request.POST)
        formset = ChoiceFormSet(request.POST)
        if poll_form.is_valid() and formset.is_valid():
            poll = poll_form.save()
            choices = formset.save(commit=False)
            for choice in choices:
                choice.poll = poll
                choice.save()
            return redirect('polls:index')
    else:
        poll_form = PollForm()
        formset = ChoiceFormSet()
    return render(request, 'polls/create_poll.html', {'poll_form': poll_form, 'formset': formset})

def edit_poll(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
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

def delete_poll(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    if request.method == 'POST':
        poll.delete()
        return redirect('polls:index')
    return render(request, 'polls/delete_poll.html', {'poll': poll})

def results(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    return render(request, 'polls/results.html', {'poll': poll})

