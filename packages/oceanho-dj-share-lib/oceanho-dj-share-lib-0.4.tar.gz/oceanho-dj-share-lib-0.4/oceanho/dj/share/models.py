from django.db import models
from django.utils import timezone


class BigIntPKAbstractModel(models.Model):
    id = models.BigAutoField(primary_key=True, null=False)

    class Meta:
        abstract = True  # Set this model as Abstract


class HasTenantIdState(models.Model):
    tenant_id = models.BigIntegerField(null=True, default=None)

    class Meta:
        abstract = True  # Set this model as Abstract


class HasCreationState(models.Model):
    created_at = models.DateTimeField("The row first creation date Time.", default=timezone.now)

    class Meta:
        abstract = True  # Set this model as Abstract


class HasModificationState(models.Model):
    modified_at = models.DateTimeField("The row latest modification date Time.", null=True)

    class Meta:
        abstract = True  # Set this model as Abstract


class HasSoftDeletionState(models.Model):
    is_deleted = models.BooleanField('The row has been logistic deleted.', null=True, default=False)
    deleted_at = models.DateTimeField("The row deletion date Time.", null=True)

    class Meta:
        abstract = True  # Set this model as Abstract


class HasActivationState(models.Model):
    is_active = models.BooleanField("The row are active.", null=True, default=True)

    class Meta:
        abstract = True
