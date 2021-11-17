from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User


class HistoryModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pregancies = models.IntegerField()
    glucose = models.IntegerField()
    bp = models.IntegerField()
    skin = models.IntegerField()
    insulin = models.IntegerField()
    bmi = models.FloatField()
    dpf = models.FloatField()
    age = models.IntegerField()
    result = models.CharField(max_length=10)
    datetime = models.DateTimeField()

    def __str__(self):
        return str(self.user) + "-" + str(self.result)
