from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404

from .models import Question


def index(request):
    latest_questions = Question.objects.order_by("-pub_date")[:5]
    context = {
        "latest_questions": latest_questions,
    }
    return render(request=request, template_name="polls/index.html", context=context)


def detail(request, question_id):
    question = get_object_or_404(klass=Question, pk=question_id)
    context = {"question": question}
    return render(request=request, template_name="polls/detail.html", context=context)


def results(request, question_id):
    return HttpResponse(
        content=f"You are looking at the results of question {question_id}"
    )


def vote(request, question_id):
    return HttpResponse(
        content=f"You are voting on question {question_id}"
    )
