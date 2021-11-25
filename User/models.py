from django.db import models
from django.contrib.auth.models import BaseUserManager
from .services import HashService


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, password, nickname, gold):
        user = self.model(username=username,
                          password=HashService.hash_string_to_password(
                              password),
                          nickname=nickname,
                          gold=gold)
        user.save(using=self._db)
        return user

    def create_user(self, username, password, nickname, gold):
        return self._create_user(username, password, nickname, gold)


class User(models.Model):
    user_idx = models.AutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=45)
    password = models.CharField(max_length=64)
    nickname = models.CharField(max_length=45)
    gold = models.IntegerField(default=0)

    objects = UserManager()

    is_anonymous = None
    is_authenticated = None

    EMAIL_FIELD = 'username'
    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = []

    class Meta:
        managed = False
        db_table = 'user'
