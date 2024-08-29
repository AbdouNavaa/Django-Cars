from django.contrib import admin

from .models import *



class CreatorAdmin(admin.ModelAdmin):
    list_display = ('id','user',)

admin.site.register(Creator,CreatorAdmin)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title','user',)
admin.site.register(Review,ReviewAdmin)

class CarAdmin(admin.ModelAdmin):
    list_display = ('title','seller','likes')
admin.site.register(Car,CarAdmin)

class SellerAdmin(admin.ModelAdmin):
    list_display = ('name','max_price',)
admin.site.register(Seller,SellerAdmin)

class trimAdmin(admin.ModelAdmin):
    list_display = ('name','model',)
admin.site.register(Trim,trimAdmin)


class modelAdmin(admin.ModelAdmin):
    list_display = ('name','seller',)
admin.site.register(Car_model,modelAdmin)


class CylinderAdmin(admin.ModelAdmin):
    list_display = ('id','name')
admin.site.register(Cylinder,CylinderAdmin)

class Fuel_TypeAdmin(admin.ModelAdmin):
    list_display = ('id','name')
admin.site.register(Fuel_Type,Fuel_TypeAdmin)

class ColorAdmin(admin.ModelAdmin):
    list_display = ('id','name')
admin.site.register(Color,ColorAdmin)

class ImageAdmin(admin.ModelAdmin):
    list_display = ('id','car')
admin.site.register(CarImage,ImageAdmin)

class ComAdmin(admin.ModelAdmin):
    list_display = ('id','car','user')
admin.site.register(Comment,ComAdmin)