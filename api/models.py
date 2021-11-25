import string
from random import choices
from django.db import models
from URLShortner import settings


class Link(models.Model):
    original_link=models.URLField()
    short_link=models.URLField(null=True,blank=True)

    def shortner(self):
        while True:
            str=''.join(choices(string.ascii_letters+string.digits,k=6))
            new_link=settings.HOST_URL+'/'+str

            if not Link.objects.filter(short_link=new_link).exists():
                break;
        return new_link

    def save(self,*args,**kwargs):
        if not self.short_link:
            new_link=self.shortner()
            self.short_link=new_link
        return super().save(*args,**kwargs)