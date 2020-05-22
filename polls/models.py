from django.db import models
from account.models import CustomUser

class Poll(models.Model):
    poll_question = models.CharField(max_length=300)
    poll_creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="poll_creator")
    poll_expiration_date = models.DateField()
    poll_created = models.DateField(auto_now=True)


class Choice(models.Model):
    choice_name = models.CharField(max_length=30)
    poll_name = models.ForeignKey("Poll", on_delete=models.CASCADE)


