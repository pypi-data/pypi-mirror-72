=====================
oceanho-dj-shared-lib
=====================

oceanho-dj-shared-lib 是个人(OceanHo)的 django 通用 library, 包括 model, utils, middleware, validators 等等.

Quick start
-----------

1. Define your models like this::

    import django.db.models
    from oceanho.dj.shared.models import BigIntPKAbstractModel
    from oceanho.dj.shared.models import HasCreationState
    from oceanho.dj.shared.models import HasModificationState
    from oceanho.dj.shared.models import HasSoftDeletionState
    from oceanho.dj.shared.models import HasTenantIdState
    from oceanho.dj.shared.models import HasActivationState

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


