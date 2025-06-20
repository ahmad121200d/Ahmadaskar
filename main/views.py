from django.shortcuts import render, get_object_or_404, redirect
from .models import Mall, UserProfile, Product
from .forms import UserProfileForm, MallForm, ProductForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

@login_required(login_url='login')
def home(request):
    return redirect('mall_list')

@login_required(login_url='login')
def mall_list(request):
    malls = Mall.objects.all()
    return render(request, 'main/mall_list.html', {'malls': malls})

@login_required(login_url='login')
def profile_view(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        if 'delete_image' in request.POST:
            profile.image.delete()
            profile.image = None
            profile.save()
            return redirect('profile')

        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save()
            user.username = form.cleaned_data['username']
            user.email = form.cleaned_data['email']
            user.save()
            return render(request, 'main/profile.html', {'user': user, 'profile': profile, 'form': form, 'success': True})
    else:
        form = UserProfileForm(instance=profile, initial={'username': user.username, 'email': user.email})
    
    return render(request, 'main/profile.html', {'user': user, 'profile': profile, 'form': form})

@login_required(login_url='login')
def add_mall(request):
    if request.method == 'POST':
        form = MallForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('mall_list')
    else:
        form = MallForm()
    return render(request, 'main/mall_form.html', {'form': form, 'is_edit': False})

@login_required(login_url='login')
def edit_mall(request, mall_id):
    mall = get_object_or_404(Mall, id=mall_id)
    if request.method == 'POST':
        if 'delete_image' in request.POST:
            mall.image.delete()
            mall.image = None
            mall.save()
            return redirect('edit_mall', mall_id=mall.id)

        form = MallForm(request.POST, request.FILES, instance=mall)
        if form.is_valid():
            form.save()
            return redirect('mall_list')
    else:
        form = MallForm(instance=mall)
    return render(request, 'main/mall_form.html', {'form': form, 'is_edit': True, 'mall': mall})

@login_required(login_url='login')
def mall_products(request, mall_id):
    mall = get_object_or_404(Mall, id=mall_id)
    products = mall.products.all()
    return render(request, 'main/mall_products.html', {'mall': mall, 'products': products})

@login_required(login_url='login')
def add_product(request, mall_id):
    mall = get_object_or_404(Mall, id=mall_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.mall = mall
            product.save()
            return redirect('mall_products', mall_id=mall.id)
    else:
        form = ProductForm()
    return render(request, 'main/product_form.html', {'form': form, 'mall': mall, 'is_edit': False})

@login_required(login_url='login')
def edit_product(request, mall_id, product_id):
    mall = get_object_or_404(Mall, id=mall_id)
    product = get_object_or_404(Product, id=product_id, mall=mall)
    if request.method == 'POST':
        if 'delete_image' in request.POST:
            product.image.delete()
            product.image = None
            product.save()
            return redirect('edit_product', mall_id=mall.id, product_id=product.id)
            
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('mall_products', mall_id=mall.id)
    else:
        form = ProductForm(instance=product)
    return render(request, 'main/product_form.html', {'form': form, 'mall': mall, 'is_edit': True, 'product': product})

@login_required(login_url='login')
def delete_product(request, mall_id, product_id):
    mall = get_object_or_404(Mall, id=mall_id)
    product = get_object_or_404(Product, id=product_id, mall=mall)
    if request.method == 'POST':
        product.delete()
        return redirect('mall_products', mall_id=mall.id)
    return render(request, 'main/product_confirm_delete.html', {'mall': mall, 'product': product})

@login_required(login_url='login')
def delete_mall(request, mall_id):
    mall = get_object_or_404(Mall, id=mall_id)
    if request.method == 'POST':
        mall.delete()
        return redirect('mall_list')
    return render(request, 'main/mall_confirm_delete.html', {'mall': mall})

def login_view(request):
    message = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            message = 'اسم المستخدم أو كلمة المرور غير صحيحة.'
    return render(request, 'main/login.html', {'message': message})

def logout_view(request):
    logout(request)
    if request.method == 'POST':
        return Response({'success': True, 'message': 'تم تسجيل الخروج بنجاح'})
    return redirect('login')

class LoginAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({'success': True, 'message': 'تم تسجيل الدخول بنجاح'})
        else:
            return Response({'success': False, 'message': 'اسم المستخدم أو كلمة المرور غير صحيحة'}, status=status.HTTP_401_UNAUTHORIZED)
