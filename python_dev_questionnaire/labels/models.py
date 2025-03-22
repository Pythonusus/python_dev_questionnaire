from django.db import models


class Label(models.Model):
    name = models.CharField(
        verbose_name='Метка',
        max_length=150,
        unique=True,
        blank=False,
        null=False,
    )
    created_at = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Метка'
        verbose_name_plural = 'Метки'

    def __str__(self):
        return self.name
