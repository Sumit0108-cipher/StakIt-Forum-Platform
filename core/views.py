from django.shortcuts import render, redirect, get_object_or_404
from .forms import QuestionForm, AnswerForm
from .models import Question
from .models import Tag
from .models import Answer
from notifications.models import Notification
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseRedirect
from .models import Answer
from django.db.models import Count
# Create your views here.


def home(request):
    sort_by = request.GET.get('sort', 'newest')  # default to newest

    if sort_by == 'unanswered':
        questions = Question.objects.annotate(answer_count=Count('answers')).filter(answer_count=0).order_by('-created_at')
    else:  # 'newest'
        questions = Question.objects.all().order_by('-created_at')

    return render(request, 'core/question_list.html', {
        'questions': questions,
        'sort_by': sort_by,
    })
@login_required
def ask_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user
            question.save()

             # Custom tag handling
            raw_tags = form.cleaned_data['tags']  # comma-separated string
            tag_names = [t.strip() for t in raw_tags.split(',') if t.strip()]
            for tag_name in tag_names:
                tag_obj, _ = Tag.objects.get_or_create(name=tag_name)
                question.tags.add(tag_obj)


            return redirect('home')  # or to the question detail
    else:
        form = QuestionForm()

    return render(request, 'core/ask_question.html', {'form': form})


def question_detail(request, pk):
    question = get_object_or_404(Question, pk=pk)

    if request.user.is_authenticated:
        Notification.objects.filter(
            recipient=request.user,
            url=request.path,
            is_read=False
        ).update(is_read=True)

    answers = question.answers.all().order_by('-created_at')

    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.user = request.user
            answer.save()

            # ✅ Send notification to question owner (if not self)
            if question.user != request.user:
                Notification.objects.create(
                    recipient=question.user,
                    message=f"{request.user.username} answered your question.",
                    url=question.get_absolute_url()  # make sure Question model has get_absolute_url
                )

            return redirect('question_detail', pk=pk)
    else:
        form = AnswerForm()

    return render(request, 'core/question_detail.html', {
        'question': question,
        'answers': answers,
        'form': form
    })

@login_required
def accept_answer(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id)
    question = answer.question
    # Only the user who asked the question can accept an answer
    if question.user != request.user:
        return HttpResponseForbidden("You are not allowed to accept this answer.")

    # Unmark any previously accepted answers
    question.answers.filter(is_accepted=True).update(is_accepted=False)

    # Mark the selected one
    answer.is_accepted = True
    answer.save()

    return HttpResponseRedirect(question.get_absolute_url())



@login_required
def upvote_answer(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)

    # Prevent self-upvote if desired
    # if request.user == answer.user:
    #     return redirect(answer.question.get_absolute_url())

    answer.votes += 1
    answer.save()
    return redirect(answer.question.get_absolute_url())

# delete_question
@login_required
def delete_question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.user != question.user:
        return HttpResponseForbidden("You are not allowed to delete this question.")

    if request.method == 'POST':
        question.delete()
        return redirect('home')

    return render(request, 'core/confirm_delete.html', {'question': question})