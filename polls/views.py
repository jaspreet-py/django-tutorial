from django.contrib import messages
from django.db.models import F
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from typing import Any, Dict, Optional

from .models import Question, Choice


class IndexView(generic.ListView):
    template_name: str = "polls/index.html"
    context_object_name: Optional[str] = "latest_questions"

    def get_queryset(self):
        """Return the latest 5 published questions"""
        return Question.objects.filter(pub_date__lte=timezone.now())[:5]


class DetailView(generic.DetailView):
    """Show voting page for the given question ID"""

    model = Question
    template_name: str = "polls/detail.html"

    def get_queryset(self):
        """Exclude any questions that aren't published yet"""
        return Question.objects.filter(pub_date__lte=timezone.now())

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["other_questions"] = Question.objects.all().exclude(
            pk=self.kwargs.get("pk")
        )
        return context


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
        messages.error(request=request, message="You didn't select a choice!")
        return redirect(
            to=reverse(
                viewname="polls:detail",
                kwargs={"pk": question_id},
            )
        )

    selected_choice.votes = F("votes") + 1
    selected_choice.save()

    # Returning a redirect to prevent data from being submitted
    # twice in case user hits the back button
    return redirect(to=reverse(viewname="polls:results", kwargs={"pk": question.id}))
