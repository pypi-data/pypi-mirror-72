====================
oceanho-dj-share-lib
====================

oceanho-dj-share-lib 是个人(OceanHo)的 django 通用 library, 包括 model, utils, middleware, validators 等等.

Quick start
-----------

1. Define your models like this::

    import django.db.models
    from oceanho.dj.share.models import BigIntPKAbstractModel
    from oceanho.dj.share.models import HasCreationState
    from oceanho.dj.share.models import HasModificationState
    from oceanho.dj.share.models import HasSoftDeletionState
    from oceanho.dj.share.models import HasTenantIdState
    from oceanho.dj.share.models import HasActivationState

    class MyUser(BigIntPKAbstractModel, HasCreationState):
        email = models.CharField(max_length=200)


2. Execute `./manage.py makemigrations && ./mange.py migrate`, then go to your db, your tables like this::

    +------------+--------------+------+-----+---------+----------------+
    | Field      | Type         | Null | Key | Default | Extra          |
    +------------+--------------+------+-----+---------+----------------+
    | id         | bigint       | NO   | PRI | NULL    | auto_increment |
    | created_at | datetime(6)  | NO   |     | NULL    |                |
    | name       | varchar(200) | NO   |     | NULL    |                |
    +------------+--------------+------+-----+---------+----------------+


