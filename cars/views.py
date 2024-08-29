from django.shortcuts import render,get_object_or_404, redirect
from .models import *
# Create your views here.

def home(request):
    return render(request, 'home.html', {})
from django.core.paginator import Paginator


def trendings(request):
    # Obtenez les valeurs des filtres depuis la requête GET
    type_of_cylinder = request.GET.get('type', '')
    year = request.GET.get('year', '')
    model = request.GET.get('model', '')
    price = request.GET.get('price', '')

    # Filtrer les voitures en fonction des conditions
    cars = Car.objects.filter(likes__gt=10)
    
    if type_of_cylinder:
        cars = cars.filter(type_of_cylinder__name__icontains=type_of_cylinder)
    
    if year:
        print('=======year:=========',year)
        cars = cars.filter(year=year)
    
    if model:
        print('=======price:=========',model)
        cars = cars.filter(model__name__icontains=model)
    
    if price:
        print('=======price:=========',price)
        cars = cars.filter(price=price)

    paginator = Paginator(cars, 3)  # Affichez 3 voitures par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'type_of_cylinder': type_of_cylinder,  # Pour préremplir le champ
        'year': year, # Pour préremplir le champ
        'model': model,  # Pour préremplir le champ
        'price': price  # Pour préremplir le champ
    }
    
    return render(request, 'trending.html', context)


def auctions(request):
    sellers = Seller.objects.all()
    cars = Car.objects.all()
    paginator1 = Paginator(sellers, 7)  # Affichez 3 voitures par page
    paginator = Paginator(cars, 3)  # Affichez 3 voitures par page
    page_number1 = request.GET.get('page1')
    page_number = request.GET.get('page')
    page_obj1 = paginator1.get_page(page_number1)
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj1': page_obj1,
        'page_obj': page_obj,
        'cars':cars,
        'sellers':sellers 
        }
    return render(request, 'auctions.html', context)

def seller_cars(request):
    # Get date range from request
    seller = request.GET.get('seller')
    print('seller',seller)
    # Base query for courses with signed_status 'effectué' and payment status 'en attente'
    cars = Car.objects.filter(seller=seller)
    sellers = Seller.objects.all()
    paginator1 = Paginator(sellers, 7)  # Affichez 3 voitures par page
    paginator = Paginator(cars, 3)  # Affichez 3 voitures par page
    page_number1 = request.GET.get('page1')
    page_number = request.GET.get('page')
    page_obj1 = paginator1.get_page(page_number1)
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj1': page_obj1,
        'page_obj': page_obj,
        'cars':cars,
        'sellers':sellers ,
        'seller':seller ,
        }
    return render(request, 'auctions.html', context)
def reviews(request):
    return render(request, 'reviews.html', {})
    
from django.contrib import messages
from .models import Car, Seller
def add_car(request):
    if request.method == 'POST':
        # Créer la voiture
        car = Car.objects.create(
            title=request.POST['title'],
            seller=Seller.objects.get(id=request.POST['seller']),
            model=Car_model.objects.get(id=request.POST['model']),
            trim=Trim.objects.get(id=request.POST['trim']),
            InteriorColor=Color.objects.get(id=request.POST['InteriorColor']),
            ExteriorColor=Color.objects.get(id=request.POST['ExteriorColor']),
            fuel_type=Fuel_Type.objects.get(id=request.POST['fuel_Type']),
            type_of_cylinder=Cylinder.objects.get(id=request.POST['type_of_cylinder']),
            year=request.POST['year'],
            price=request.POST['price'],
            speed=request.POST['speed'],
        )

        # Gérer les images
        for image in request.FILES.getlist('images'):
            CarImage.objects.create(car=car, image=image)

        messages.success(request, 'Car saved successfully')
        return redirect('home')

    # Récupération des données pour le formulaire
    context = {
        'sellers': Seller.objects.all(),
        'cylinders': Cylinder.objects.all(),
        'trims': Trim.objects.all(),
        'colors': Color.objects.all(),
        'fuel_Types': Fuel_Type.objects.all(),
        'models': Car_model.objects.all(),
        'values': request.POST
    }
    return render(request, 'add_car.html', context)

from django.http import JsonResponse

def load_models(request):
    seller_id = request.GET.get('seller_id')
    models = Car_model.objects.filter(seller_id=seller_id).all()
    return JsonResponse(list(models.values('id', 'name')), safe=False)

def load_trims(request):
    model_id = request.GET.get('model_id')
    trims = Trim.objects.filter(model_id=model_id).all()
    return JsonResponse(list(trims.values('id', 'name')), safe=False)

def car_details(request,id):
    car = Car.objects.get(id = id)
    cars = Car.objects.filter(seller = car.seller)
    update = False
    comments = Comment.objects.filter(car=car)
    context = {'car':car ,"cars":cars,'comments':comments,'update':update}
    return render(request, 'details.html', context)

def add_like(request,id):
    car = Car.objects.get(id=id)
    car.likes += 1  # Increment the car's likes
    car.save()
    return redirect('trendings')

def add_carImage(request, id):
    car = Car.objects.get(id = id)
    if request.method == 'GET':
        return render(request, 'add_carImage.html', {'id':id})

    if request.method == 'POST':
        # Récupération des données du formulaire
        image = request.FILES.get('image')  # Notez l'utilisation de request.FILES


        for image in request.FILES.getlist('images'):
            CarImage.objects.create(car=car, image=image)

        messages.success(request, 'CarImage saved successfully')

        return redirect('car_details',id)

from django.contrib.auth.decorators import login_required


@login_required
def add_comment(request, id):
    car = get_object_or_404(Car, id=id)
    update = False
    try:
        creator = Creator.objects.get(user=request.user)
        print('ok')
    except Creator.DoesNotExist:
        print('no')
        
        # Gérer le cas où l'utilisateur connecté n'a pas de profil Author
        return redirect('car_details',id=id)  # Rediriger vers une page de création de profil ou afficher un message d'erreur

    if request.method == 'POST':
        print('ok1')
        description = request.POST.get('comment_box', '')
        if description:
            # Créer et sauvegarder le commentaire
            Comment.objects.create(
                user=creator,
                car=car,
                description=description
            )


    # Récupérer les commentaires associés à la vidéo
    comments = Comment.objects.filter(car=car)
    return redirect('car_details',id=id)

from django.contrib import messages
@login_required
def update_comment(request, car_id, c_id):
    car = get_object_or_404(Car, id=car_id)
    comment = get_object_or_404(Comment, id=c_id)

    try:
        user = Creator.objects.get(user=request.user)
    except user.DoesNotExist:
        # Gérer le cas où l'utilisateur connecté n'a pas de profil user
        messages.error(request, "Vous devez avoir un profil pour commenter.")
        return redirect('car_details', id=car_id)

    if request.method == 'POST':
        description = request.POST.get('comment_box', '')
        if description:
            # Vérifier si l'utilisateur est autorisé à mettre à jour le commentaire
            if request.user.id == comment.user.id +1:
                comment.description = description
                comment.save()
                messages.success(request, "Commentaire mis à jour avec succès.")
                print("Commentaire mis à jour avec succès.")
            else:
                messages.error(request, "Vous n'êtes pas autorisé à mettre à jour ce commentaire.")
                print("Vous n'êtes pas autorisé à mettre à jour ce commentaire.")

    # Récupérer les commentaires associés à la vidéo
    return redirect('car_details',car_id)


@login_required
def delete_comment(request, car_id,c_id):
    car = get_object_or_404(Car, id=car_id)
    comment = get_object_or_404(Comment, id=c_id)

    try:
        user = Creator.objects.get(user=request.user)
        print('user',request.user)
        print('ok')
    except Creator.DoesNotExist:
        print('no')
        
        # Gérer le cas où l'utilisateur connecté n'a pas de profil user
        return redirect('car_details',id=car_id)  # Rediriger vers une page de création de profil ou afficher un message d'erreur
    user = Creator.objects.get(user=request.user)
    print('User:==========',user.id)
    if user.id == comment.user.id:
        print('ok1')
        comment.delete()
        messages.success(request, "Commentaire Supprimer avec succès.")
            # Incrémenter le nombre de commentaires de l'auteur
        # user.total_comments -= 1
        # author.save()
    else:
        print('Tu ne peux pas supprimer cette commentaire',request.user,comment.user)
    comments = Comment.objects.filter(car=car)
    
    return redirect('car_details',car_id)



def to_Update(request,id,c_id):
    car = Car.objects.get(id=id)
    comment = Comment.objects.get(id=c_id)
    update = True
    comments = Comment.objects.filter(car=car)
    print('abdou',comment.id,comment)
    messages.success(request, "Tu peux commencer.")
    
    cars = Car.objects.filter(seller = car.seller)
    context={"cars":cars,'car':car,'comments':comments,'comment':comment,'update':update}
    return render(request, 'details.html', context) 

