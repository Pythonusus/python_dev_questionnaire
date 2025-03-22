from django.urls import path

from python_dev_questionnaire.questions.views import (
    QuestionDetailView,
    QuestionsIndexView,
)

urlpatterns = [
    path('', QuestionsIndexView.as_view(), name='questions_index'),
    path('<int:pk>/', QuestionDetailView.as_view(), name='question_detail'),
]
