"""
Factories for generating test data.
"""

import factory
import factory.random
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

from python_dev_questionnaire.categories.models import Category
from python_dev_questionnaire.labels.models import Label
from python_dev_questionnaire.questions.models import Question

# Set seed for random data generation to ensure consistent
# test data across different test runs.
SEED = 4321
factory.random.reseed_random(SEED)


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.Faker('user_name')
    # Users in tests are always created with the same hashed password
    password = factory.LazyFunction(lambda: make_password('testpass!123'))
    email = factory.Faker('email')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda n: f'Category {n}')


class LabelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Label

    name = factory.Sequence(lambda n: f'Label {n}')


class QuestionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Question

    question = factory.Faker('sentence')
    answer = factory.Faker('sentence')
    category = factory.SubFactory(CategoryFactory)

    @factory.post_generation
    def labels(self, created, extracted, **kwargs):
        """
        Post-generation hook for handling question labels.

        Executes if the question is created successfully.
        If labels are provided, add them to the question.
        If no labels are provided and create_default is True,
        create a default label and add it to the question.
        Otherwise, leave labels empty.

        Args:
            created (bool): Whether the question was created successfully.
            extracted (iterable, optional): Labels sequence to add to question.
            **kwargs: Additional arguments passed to the hook.
        """
        if not created:
            return

        # Get create_default from kwargs, default to True if not provided
        create_default = kwargs.get('create_default', True)

        if extracted:
            # Add the provided labels to the question
            self.labels.set(extracted)
        elif create_default:
            # Create and add a default label
            label = LabelFactory()
            self.labels.add(label)

    @classmethod
    def create_with_no_labels(cls, **kwargs):
        """
        Create a question instance with no associated labels.

        Args:
            **kwargs: Additional fields to set on the question instance.

        Example:
            question = QuestionFactory.create_with_no_labels()
        """
        return cls.create(labels=None, labels__create_default=False, **kwargs)
