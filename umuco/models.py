from django.db import models

class Raport( models.Model):
    """
    a model for a NaweNuze report
    """
    date = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
    lampes_rechargees = models.IntegerField(default=0)
    lampes_vendues = models.IntegerField(default=0)
    montant = models.IntegerField(default=0)
    groupe = models.CharField( max_length = 60 , blank=True , default="Anonymous group" )

    def __unicode__(self):
        return u'%s %s %s %s' % (self.date , self.lampes_vendues, self.lampes_rechargees, self.montant)

