import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Question


def create_question(question_text: str, days: int):
    """
    Create a question with the given 'question_text', published given
    number of 'days' offset to now (negative for questions published in
    the past, while positive for questions yet to be published)
    """
    pub_date = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=pub_date)


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_date(self):
        """was_published_recently() returns False for questions whose pub_date is in the future"""
        pub_date = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=pub_date)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """was_published_recently() returns False for questions whose pub_date is older than 1 day"""
        pub_date = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=pub_date)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """was_published_recently() returns True for questions whose pub_date is within the last day"""
        pub_date = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=pub_date)
        self.assertIs(recent_question.was_published_recently(), True)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """If no questions exist, an appropriate message is displayed"""
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "no polls are available")
        self.assertQuerysetEqual(response.context["latest_questions"], [])

    def test_past_question(self):
        """Questions with a pub_date in the past are displayed on the index page"""
        question = create_question(question_text="Ye jhakkas dikhega re biddu", days=-1)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_questions"], [question])

    def test_future_question(self):
        """Questions with a pub_date in the future are not displayed on the index page"""
        create_question(question_text="Ye nhi dikhega re biddu", days=1)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_questions"], [])

    def test_future_and_past_questions(self):
        """If questions exist with both past and future pub_dates, only questions with past pub_dates are diplayed"""
        question = create_question(question_text="Aila, ye question dikhega", days=-5)
        create_question(question_text="magar ye nhi dikhega!", days=50)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_questions"], [question])

    def test_multiple_past_questions(self):
        """Index page may display multiple questions"""
        question1 = create_question(question_text="Mai dikhuga na bhaiya??", days=-100)
        question2 = create_question(
            question_text="Han chhote, bilkul meri tarah tu bhi dikhega", days=-10
        )
        response = self.client.get(reverse("polls:index"))
        # While asserting, it is important to order the test question objects according to how
        # the fetched queryset will be ordered. Hence, owing to this, an assertion on [question1, question2]
        # would fail, as the fetched queryset will be ordered by "pub_date" in a descending order
        self.assertQuerysetEqual(
            response.context["latest_questions"], [question2, question1]
        )


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """The detail view of a question with a future pub_date returns a 404 not found"""
        future_question = create_question(
            question_text="Ayy merko kaise request kr rha h be?", days=1
        )
        url = reverse(viewname="polls:detail", args=(future_question.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """The detail view of a question with pub_date in the past returns the requested question object"""
        past_question = create_question(
            question_text="Accha theek h, merko kr skta h request!", days=-1
        )
        url = reverse(viewname="polls:detail", args=(past_question.pk,))
        response = self.client.get(url)
        self.assertEqual(response.context["question"], past_question)
