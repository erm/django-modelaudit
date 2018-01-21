import json

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.conf import settings

from modelaudit.middleware import get_current_user


class AuditRecord(models.Model):

    class Meta:
        verbose_name = 'Audit Record'
        verbose_name_plural = 'Audit Records'

    def __str__(self):
        return 'AuditRecord @ {}'.format(self.created_at)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    changed_fields = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='audit_records',
        on_delete=models.CASCADE,
        null=True,
        editable=False
    )


class AuditRecordMixin(models.Model):

    """
    Mixin for logging model field changes.
    """

    class Meta:
        abstract = True

    audit_records = GenericRelation(AuditRecord)

    def get_revision_field_names(self):
        return [f.name for f in self._meta.get_fields()]

    def save(self, *args, **kwargs):
        _self = type(self).objects.get(pk=self.pk) if self.pk else None
        super(AuditRecordMixin, self).save(*args, **kwargs)
        if _self:
            changed_fields = {}
            for field in self.get_revision_field_names():
                old, new = getattr(_self, field), getattr(self, field)
                if old != new:
                    changed_fields[str(field)] = {str(old): str(new)}
            if changed_fields:
                AuditRecord.objects.create(
                    content_object=self,
                    changed_fields=json.dumps(changed_fields),
                    user=get_current_user()
                )
