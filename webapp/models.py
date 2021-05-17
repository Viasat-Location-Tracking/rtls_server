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
        return "Tag %d at %s" % (self.tag_id, self.timestamp)

class Tag(models.Model):
    tag_id = models.IntegerField()
    serial_num = models.CharField(max_length=150)
    valid_after = models.DateTimeField()
    valid_before = models.DateTimeField(null=True)


    def __str__(self):
        return "Tag %d, serial number %s" % (self.tag_id, self.serial_num)

class ClinicItem(models.Model):
    tag_id = models.IntegerField()
    serial_num = models.CharField(max_length=150)
    added_to_clinic = models.DateTimeField()
    removed_from_clinic = models.DateTimeField(null=True)
    from_zone = ArrayField(models.CharField(max_length=150))
    problem = models.CharField(max_length=1000)

    def __str__(self):
        return "Tag %d, serial number %s" % (self.tag_id, self.serial_num)