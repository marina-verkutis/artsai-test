from django.db import models


class View(models.Model):
    objects = None
    reg_time = models.DateTimeField(blank=True, null=True, db_index=True)
    uid = models.CharField('uid', max_length=36, db_index=True)
    fc_imp_chk = models.IntegerField()  # число предшествующих показов
    fc_time_chk = models.IntegerField()  # время с момента последнего показа
    utmtr = models.IntegerField()
    mm_dma = models.IntegerField(db_index=True)
    osName = models.CharField('osName', max_length=50)
    model = models.CharField('model', max_length=50)
    hardware = models.CharField('hardware', max_length=50)
    site_id = models.CharField('site_id', max_length=100, db_index=True)

    def __str__(self):
        return self.uid


class Event(models.Model):
    objects = None
    uid = models.CharField('uid', max_length=36, db_index=True)
    tag = models.CharField('tag', max_length=50, db_index=True)

    def __str__(self):
        return self.uid
