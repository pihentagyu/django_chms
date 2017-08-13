from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from model_utils.managers import InheritanceManager
import os

from django.contrib.auth.models import User
from cities_local.models import Country, Region, City
# Create your models here.



class Family(models.Model):
    def get_image_path(instance, filename):
        return os.path.join('photos', str(instance.id), filename)

    class Meta:
        verbose_name_plural = 'Families'
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(User, blank=True, null=True, on_delete=models.SET_NULL)
    family_name = models.CharField(max_length=50)
    address1 = models.CharField(blank=True, max_length=255)
    address2 = models.CharField(blank=True, max_length=255)
    postal_code = models.CharField(blank=True, max_length=15)
    country = models.ForeignKey(Country, blank=True, null=True)
    region = models.ForeignKey(Region, blank=True, null=True)
    city = models.ForeignKey(City, blank=True, null=True)

    membership_status = models.CharField(max_length=2, choices=settings.MEMBERSHIP_TYPES, default='FM')
    notes = models.TextField(blank=True)
    image = models.ImageField(upload_to=get_image_path, blank=True, null=True)
    image_sm = ImageSpecField(source='image',
                                    processors=[ResizeToFill(300, 200)],
                                    format='JPEG',
                                    options={'quality': 60})

    def get_adults(self):
        #return [member for member in self.member_set.all() if hasattr(member, 'adult')]
        return [member for member in self.member_set.all() if hasattr(member, 'adult')]

    def get_children(self):
        return [member for member in self.member_set.all() if hasattr(member, 'child')]
    
    def get_children_names(self):
        return [member.first_name for member in self.member_set.all() if hasattr(member, 'child')]
   
    def __str__(self):
        return self.family_name

    def get_absolute_url(self):
        return reverse('families:family_detail', kwargs={
            'pk': self.id,
            })

class Member(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female')
    )
    #class Meta:
    #    abstract = True
    family = models.ForeignKey(Family) 
    objects = InheritanceManager()
    title = models.CharField(blank=True, max_length=15)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(blank=True, max_length=255)
    last_name = models.CharField(max_length=50)
    suffix = models.CharField(blank=True, max_length=15)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    birth_date = models.DateField(blank=True, null=True)
    membership_status = models.CharField(max_length=2, choices=settings.MEMBERSHIP_TYPES, default='FM')
    date_joined = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True)
    def __str__(self):
        return '%s, %s' % (self.last_name, self.first_name)

    def get_member_type(self):
        if getattr(self, 'adult'):
            return 'a'
        else:
            return 'd'

    def get_absolute_url(self):
        member_type = self.get_member_type()
        return reverse('families:member_detail', kwargs={
            'family_pk': self.family_id,
            'member_type': member_type,
            'member_pk': self.id,
            })
    #def save(self, *args, **kwargs):
    #    self.last_name = self.family.family_name
    #    super(Member, self).save(*args, **kwargs)


class Adult(Member):
    occupation = models.CharField(blank=True, max_length=255)
    workplace = models.CharField(blank=True, max_length=255)
    work_address = models.CharField(blank=True, max_length=255)
    marital_status = models.CharField(blank=True, max_length=20)

    class Meta:
        ordering = ['id',]

    def get_absolute_url(self):
        return reverse('families:member_detail', kwargs={
            'family_pk': self.family_id,
            'member_type': 'a',
            'member_pk': self.id,
            })

class Child(Member):
    school = models.CharField(blank=True, max_length=255)

    class Meta:
        verbose_name_plural = 'Children'
        #    ordering = ['birth_date', 'id']

    def get_absolute_url(self):
        return reverse('families:member_detail', kwargs={
            'family_pk': self.family_id,
            'member_type': 'd',
            'member_pk': self.id,
            })
    def age(self):
        from families.templatetags.family_extras import age_calc
        if self.birth_date:
            return '{} years'.format(age_calc(self.birth_date))
        else:
            return



