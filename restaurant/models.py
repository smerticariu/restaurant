from __future__ import unicode_literals
from django.db import models
from django.core.urlresolvers import reverse
import datetime
from datetime import datetime

ORDER_PROCESSING = 0
ORDER_SHIPPING = 1
ORDER_ENDED = 2

STATUS_ORDER = (
    (ORDER_PROCESSING, 'Procesing'),
    (ORDER_SHIPPING, 'Shiping'),
    (ORDER_ENDED, 'Ended'),
)





class Menu (models.Model):
    title=models.CharField(max_length=500)
    dish1=models.CharField(max_length=500)
    dish2=models.CharField(max_length=500)
    desert=models.CharField(max_length=500)
    date_day=models.DateField(blank=True, null=True,auto_now_add=True)

    def get_absolute_ulr (self):
        return reverse('restaurant:detail',kwargs={'pk':self.pk})

    def __unicode__(self):
        return self.title + " ----- " + str(self.date_day)



class Order (models.Model):
    title=models.ForeignKey(Menu)
    name=models.CharField(max_length=255)
    email=models.EmailField(max_length=100)
    phone=models.CharField(max_length=100)
    adress=models.CharField(max_length=500)
    status = models.IntegerField(default=0, choices=STATUS_ORDER)
    raiting = models.FloatField(default=0)
    date_order=models.DateTimeField(blank=True, null=True, auto_now_add=True)

    def __unicode__(self):
         return '%s - %s' % (self.name, self.title)


