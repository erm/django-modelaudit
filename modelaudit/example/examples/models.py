from django.db import models

from modelaudit.models import AuditRecordMixin


class Example(AuditRecordMixin, models.Model):

    class Meta:
        verbose_name = 'Example'
        verbose_name_plural = 'Examples'

    def __str__(self):
        return '{}'.format(self.pk)

    description = models.TextField(null=True)
