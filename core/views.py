from django.shortcuts import render, redirect
from .forms import QuestionForm

# Create your views here.


def home(request):
    return render(request, 'core/home.html')
def ask_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user
            question.save()
            form.save_m2m()

            return redirect('home')  # or to the question detail
    else:
        form = QuestionForm()

    return render(request, 'core/ask_question.html', {'form': form})
