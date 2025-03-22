# Generated by Django 5.1.6 on 2025-03-22 15:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categories', '0001_initial'),
        ('labels', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField(unique=True, verbose_name='Вопрос')),
                ('answer', models.TextField(unique=True, verbose_name='Ответ')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('category', models.ForeignKey(help_text='Категория к которой относится вопрос', on_delete=django.db.models.deletion.PROTECT, related_name='questions', to='categories.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Вопрос',
                'verbose_name_plural': 'Вопросы',
            },
        ),
        migrations.CreateModel(
            name='QuestionLabel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='labels_questions', to='labels.label', verbose_name='Метка')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_labels', to='questions.question', verbose_name='Вопрос')),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='labels',
            field=models.ManyToManyField(blank=True, help_text='Метки для данного вопроса', related_name='questions', through='questions.QuestionLabel', to='labels.label', verbose_name='Метки'),
        ),
    ]
