from django.db import models
from account.models import CustomUser


class Poll(models.Model):
    poll_question = models.CharField(max_length=300)
    poll_creator = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="poll_creator")
    poll_expiration_date = models.DateField()
    poll_created = models.DateTimeField(auto_now=True)
    poll_has_expired = models.BooleanField(default=False)

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return self.poll_question


class Choice(models.Model):
    choice_name = models.CharField(max_length=250)
    poll_name = models.ForeignKey(
        "Poll", on_delete=models.CASCADE, related_name='choices',)

    def __str__(self):
        return f"<-- {self.choice_name} -->  is the {self.id} choice of <-- {self.poll_name.poll_question} -->"


class Vote(models.Model):
    choice_id = models.ForeignKey(
        Choice, related_name='votes', on_delete=models.CASCADE)
    poll_id = models.ForeignKey(
        Poll, on_delete=models.CASCADE, related_name='poll_vote')
    voted_by = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, related_name='voters')

    # class Meta:
    #     unique_together = ("poll_id", "voted_by")

    def __str__(self):
        return str(self.choice_id)
