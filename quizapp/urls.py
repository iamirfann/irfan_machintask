from django.contrib import admin
from django.urls import path, include
from .views import QuestionView, AnswerView, AnswerSummaryView
urlpatterns = [
    path('addquestion/', QuestionView.as_view(), name='create_question'),
    path('answer/', AnswerView.as_view(), name='answer'),
    path('answersummary/', AnswerSummaryView.as_view(), name='answersummary')

]