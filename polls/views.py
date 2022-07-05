from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Question, Choice


def index(request):
    latest_questions = Question.objects.order_by("-pub_date")[:5]
    context = {
        "latest_questions": latest_questions,
    }
    return render(request=request, template_name="polls/index.html", context=context)


def detail(request, question_id):
    """Show voting page for the given question ID"""
    question = get_object_or_404(klass=Question, pk=question_id)
    context = {"question": question}
    return render(request=request, template_name="polls/detail.html", context=context)


def results(request, question_id):
    """Display results for the given question ID"""
    question: Question = get_object_or_404(Question, pk=question_id)
    return render(
        request=request,
        template_name="polls/results.html",
        context={"question": question},
    )


def vote(request, question_id):
    """Update vote count for the given question ID"""
    question: Question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice: Choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the voting form with an error message
        return render(
            request=request,
            template_name="polls/detail.html",
            context={
                "question": question,
                "error_message": "You didn't select a choice!",
            },
        )

    selected_choice.votes += 1
    selected_choice.save()

    # Returning an HTTPResponseRedirect to prevent data from being submitted
    # twice in case user hits the back button
    return HttpResponseRedirect(
        redirect_to=reverse(
            viewname="polls:results", kwargs={"question_id": question.id}
        )
    )
