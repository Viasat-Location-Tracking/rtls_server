from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class DataPoint(models.Model):
    tag_id = models.IntegerField()
    timestamp = models.DateTimeField()
    zone = ArrayField(models.CharField(max_length=150))
    x_pos = models.DecimalField(decimal_places=2, max_digits=4)
    y_pos = models.DecimalField(decimal_places=2, max_digits=4)
    button_pushed = models.BooleanField()

    def __str__(self):
        return "Tag %s at %s" % (self.tag_id, self.timestamp)