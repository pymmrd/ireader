from django.db import models

class Suggestion(models.Model):
    desc = models.textField()
    email = models.EmailField()
    submit_date = models.DateField()
