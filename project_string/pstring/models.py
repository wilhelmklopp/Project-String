from django.db import models

# Create your models here.

class Links(models.Model):
    auto_id = models.AutoField(primary_key=True)
    short = models.CharField(max_length=10, blank=True)
    long_url = models.URLField(max_length=10000)
    unique_uuid = models.CharField(max_length=36, unique=True)
    last_changed = models.DateTimeField(auto_now = True, auto_now_add = False)
    created = models.DateTimeField(auto_now = False, auto_now_add = True, editable=False)
    user_ip = models.GenericIPAddressField()
    pageviews = models.BigIntegerField()
    def __unicode__(self):
        return str(self.unique_uuid)
