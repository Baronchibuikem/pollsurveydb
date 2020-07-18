from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class AccountConfig(AppConfig):
    name = 'account'


# class ProfilesConfig(AppConfig):
#     name = 'youchooseDjango.account'
#     verbose_name = _('users')

#     def ready(self):
#         import youchooseDjango.account.signals
