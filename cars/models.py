from django.db import models
from django.utils.text import slugify
# Create your models here.
from django.contrib.auth.models import User
from django.dispatch import receiver


Gender = (
    ('Male','Male'),
    ('woman','woman'),
)
class Creator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    job = models.CharField(max_length=50)
    image  = models.ImageField(upload_to='profile/',null=True,blank=True)
    gender = models.CharField(max_length=15 , choices=Gender)
    email = models.EmailField(max_length=50)
    mobile= models.IntegerField()
    
    slug = models.SlugField(blank=True, null=True)
        
    def save(self,*args, **kwargs):
        self.slug = slugify(self.user.username)
        super(Creator,self).save(*args, **kwargs)
    def __str__(self):
        return self.user.username     
    
# from django.db.models.signals import post_save
    
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Creator.objects.create(user=instance)  
        
class Seller(models.Model):
    name = models.CharField(max_length=30)
    image  = models.ImageField(upload_to='profile/',null=True,blank=True)
    max_price = models.IntegerField(default=0)
    slug = models.SlugField(blank=True, null=True)

    def __str__(self):
        return self.name
    def save(self,*args, **kwargs):
        self.slug = slugify(self.name)
        super(Seller,self).save(*args, **kwargs)


class Cylinder(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name


class Fuel_Type(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name
class Color(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name
class Car_model(models.Model):
    name = models.CharField(max_length=50)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True, null=True)

    def __str__(self):
        return self.name
    def save(self,*args, **kwargs):
        self.slug = slugify(self.name)
        super(Car_model,self).save(*args, **kwargs)
class Trim(models.Model):
    name = models.CharField(max_length=50)
    model = models.ForeignKey(Car_model, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
from django.db import models

class Car(models.Model):
    title = models.CharField(max_length=50)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    model = models.ForeignKey(Car_model, on_delete=models.CASCADE)
    trim = models.ForeignKey(Trim, on_delete=models.CASCADE, default='')
    InteriorColor = models.ForeignKey(Color, on_delete=models.CASCADE, related_name='interior_color')
    ExteriorColor = models.ForeignKey(Color, on_delete=models.CASCADE, related_name='exterior_color')
    fuel_type = models.ForeignKey(Fuel_Type, on_delete=models.CASCADE)
    type_of_cylinder = models.ForeignKey(Cylinder, on_delete=models.CASCADE)
    year = models.FloatField(default=2020)
    price = models.FloatField(default=0)
    speed = models.FloatField(default=400)
    likes = models.IntegerField(default=10)
    slug = models.SlugField(blank=True, null=True)
    
    def __str__(self):
        return self.title
    def save(self,*args, **kwargs):
        self.slug = slugify(self.title)
        super(Car,self).save(*args, **kwargs)


class CarImage(models.Model):
    car = models.ForeignKey(Car, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='cars/')

    def __str__(self):
        return f"Image for {self.car.title}"






class Review(models.Model):
    image  = models.ImageField(upload_to='profile/',null=True,blank=True)
    description = models.CharField(max_length=200, default='')
    title = models.CharField(max_length=50)
    user = models.ForeignKey(Creator, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True, null=True)

    def __str__(self):
        return self.title
    def save(self,*args, **kwargs):
        self.slug = slugify(self.title)
        super(Review,self).save(*args, **kwargs)


class Comment(models.Model):
    user = models.ForeignKey(Creator,  on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE,)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.description      