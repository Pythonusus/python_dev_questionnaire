import pytest
from django.urls import reverse_lazy

from python_dev_questionnaire.factories import (
    CategoryFactory,
    LabelFactory,
    QuestionFactory,
)


class TestQuestionIndexPage:
    def setup_method(self):
        self.categories = CategoryFactory.create_batch(2)
        self.labels = LabelFactory.create_batch(3)
        self.questions = [
            QuestionFactory.create_with_no_labels(category=self.categories[0]),
            QuestionFactory(
                category=self.categories[0], labels=[self.labels[0]]
            ),
            QuestionFactory(
                category=self.categories[1],
                labels=[self.labels[0], self.labels[1]],
            ),
            QuestionFactory(category=self.categories[1], labels=self.labels),
        ]
        self.no_questions_text = (
            'Вопросы не найдены. Попробуйте изменить параметры фильтра.'
        )

    @pytest.mark.django_db
    def test_with_no_filters(self, client):
        response = client.get(reverse_lazy('questions_index'))
        content = response.content.decode()
        assert response.status_code == 200
        assert 'questions/questions_index.html' in [
            t.name for t in response.templates
        ]
        assert len(self.questions) == len(response.context['questions'])
        for question in self.questions:
            assert question.question in content
            assert question.answer in content
            assert question.category.name in content
            for label in question.labels.all():
                assert label.name in content

    @pytest.mark.django_db
    def test_with_category_filter_success(self, client):
        response = client.get(
            reverse_lazy('questions_index'),
            {
                'category': self.categories[0].id,
            },
        )
        assert response.status_code == 200

        # Questions with the selected category created in the setup_method
        expected_count = 2

        assert len(response.context['questions']) == expected_count
        for question in response.context['questions']:
            assert question.category.id == self.categories[0].id

    @pytest.mark.django_db
    def test_with_category_filter_fail(self, client):
        unpresent_category = CategoryFactory(name='Unpresent category')
        response = client.get(
            reverse_lazy('questions_index'),
            {
                'category': unpresent_category.id,
            },
        )
        assert response.status_code == 200
        assert len(response.context['questions']) == 0
        assert self.no_questions_text in response.content.decode()

    @pytest.mark.django_db
    def test_with_label_filter_success(self, client):
        response = client.get(
            reverse_lazy('questions_index'),
            {
                'label1': self.labels[0].id,
                'label2': self.labels[1].id,
            },
        )
        assert response.status_code == 200

        # Questions with the selected labels created in the setup_method
        expected_count = 2

        assert len(response.context['questions']) == expected_count

    @pytest.mark.django_db
    def test_with_label_filter_fail(self, client):
        unpresent_label = LabelFactory(name='Unpresent label')
        response = client.get(
            reverse_lazy('questions_index'),
            {
                'label1': unpresent_label.id,
            },
        )
        assert response.status_code == 200
        assert len(response.context['questions']) == 0
        assert self.no_questions_text in response.content.decode()

    @pytest.mark.django_db
    def test_with_category_and_label_filters_success(self, client):
        response = client.get(
            reverse_lazy('questions_index'),
            {
                'category': self.categories[1].id,
                'label1': self.labels[0].id,
                'label2': self.labels[1].id,
            },
        )
        assert response.status_code == 200

        # Questions with the selected category and label
        # created in the setup_method
        expected_count = 2

        assert len(response.context['questions']) == expected_count
        for question in response.context['questions']:
            assert question.category.id == self.categories[1].id
            question_label_ids = {label.id for label in question.labels.all()}
            assert self.labels[0].id in question_label_ids
            assert self.labels[1].id in question_label_ids

    @pytest.mark.django_db
    def test_with_category_and_label_filters_fail(self, client):
        unpresent_category = CategoryFactory(name='Unpresent category')
        unpresent_label = LabelFactory(name='Unpresent label')
        response = client.get(
            reverse_lazy('questions_index'),
            {
                'category': self.categories[0].id,
                'label1': unpresent_label.id,
            },
        )
        assert response.status_code == 200
        assert len(response.context['questions']) == 0
        assert self.no_questions_text in response.content.decode()

        response = client.get(
            reverse_lazy('questions_index'),
            {
                'category': unpresent_category.id,
                'label1': self.labels[0].id,
            },
        )
        assert response.status_code == 200
        assert len(response.context['questions']) == 0
        assert self.no_questions_text in response.content.decode()


class TestQuestionDetailPage:
    @pytest.mark.django_db
    def test_with_question_success(self, client):
        question = QuestionFactory()
        response = client.get(
            reverse_lazy('question_detail', args=[question.id])
        )
        content = response.content.decode()
        assert response.status_code == 200
        assert 'questions/question_detail.html' in [
            t.name for t in response.templates
        ]
        assert question.id == response.context['question'].id
        assert question.question in content
        assert question.answer in content
        assert question.category.name in content
        for label in question.labels.all():
            assert label.name in response.content.decode()
