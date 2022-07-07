from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from typing import Optional

from .models import Question, Choice


class IndexView(generic.ListView):
    template_name: str = "polls/index.html"
    context_object_name: Optional[str] = "latest_questions"

    def get_queryset(self):
        """Return the latest 5 published questions"""
        return Question.objects.order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    """Show voting page for the given question ID"""
    model = Question
    template_name: str = "polls/detail.html"


class ResultsView(generic.DetailView):
    """Display results for the given question ID"""
    model = Question
    template_name: str = "polls/results.html"


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

    selected_choice.votes = F("votes") + 1
    selected_choice.save()

    # Returning an HTTPResponseRedirect to prevent data from being submitted
    # twice in case user hits the back button
    return HttpResponseRedirect(
        redirect_to=reverse(
            viewname="polls:results", kwargs={"pk": question.id}
        )
    )
