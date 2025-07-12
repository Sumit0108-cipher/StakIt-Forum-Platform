from django.shortcuts import render, redirect, get_object_or_404
from .forms import QuestionForm, AnswerForm
from .models import Question
from .models import Tag

# Create your views here.


def home(request):
    questions = Question.objects.all().order_by('-created_at')
    return render(request, 'core/question_list.html', {'questions': questions})

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
    answers = question.answers.all().order_by('-created_at')

    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.user = request.user
            answer.save()
            return redirect('question_detail', pk=pk)
    else:
        form = AnswerForm()

    return render(request, 'core/question_detail.html', {
        'question': question,
        'answers': answers,
        'form': form
    })