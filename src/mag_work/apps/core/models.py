from django.db import models

class IndexBlock(models.Model):
    title = models.CharField(u'Название', max_length=255)

    text = models.TextField(u'Текст', blank=True, max_length=255)

    class Meta:
        ordering = (u'id',)
        verbose_name = u'Блок главной страницы'
        verbose_name_plural = u'Блоки главной страницы'

    def __unicode__(self):
        return self.title

