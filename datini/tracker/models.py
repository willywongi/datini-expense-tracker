from django.db.models.deletion import PROTECT
from django.db.models.fields import CharField, EmailField
from django.db.models.fields.related import ForeignKey, ManyToManyField
from djmoney.models.fields import MoneyField
from jables.models import JBModel
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
import nanoid


def generate():
    return nanoid.generate('abcdefghijklmnopqrstuvwxyz0123456789', size=10)


def generate_clan_code():
    return nanoid.generate('abcdefghijkmnopqrstuvwxyz023456789', size=6)


class Clan(JBModel):
    name = CharField(max_length=128)
    code = CharField(max_length=6, null=False, default=generate_clan_code)
    # members = User


class UserManager(BaseUserManager):
    """ To be used in conjunction with our custom User model that has
        the email field as the primary identifier.
    """

    def create_user(self, *args, **extra_field):
        """ Createsuperuser calls this method with (email, password, **extra_field).
            Socialauth pipeline calls this method with (email=email, password=password)
        """
        try:
            email, password = args
        except ValueError:
            email = extra_field.pop('email', None)
            password = extra_field.pop('password', None)

        if not email:
            raise ValueError(_('Email address is required'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_field)
        if password:
            user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.update(is_staff=True, is_superuser=True, is_active=True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """ Overwrites the base User model's id field using a varchar instead of a auto increment
        and using email as the primary unique key.
    """
    id = CharField(primary_key=True, default=generate, editable=False, max_length=64)
    username = None
    email = EmailField(_('email address'), unique=True)
    clan = ForeignKey(Clan, on_delete=PROTECT, default=None, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        else:
            return self.email


class Category(JBModel):
    title = CharField(max_length=128)

    def __str__(self):
        return self.title


class Expense(JBModel):
    who = ForeignKey(User, on_delete=PROTECT, related_name="+")
    what = CharField(max_length=255, default='', blank=True)
    how_much = MoneyField(max_digits=14, decimal_places=2, default=0, default_currency='EUR')
    category = ForeignKey(Category, on_delete=PROTECT)
