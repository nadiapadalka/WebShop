from django.http import HttpResponseRedirect, JsonResponse
from decimal import Decimal
from django.shortcuts import render
from django.contrib.auth import login, authenticate
from myapp.forms import OrderForm, RegistrationForm, LoginForm
from myapp.models import Category, Product, Cart, CartItem, Order
from django.urls import reverse
from django.core.paginator import Paginator

# Create your views here.

def main_page(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    categories = Category.objects.all()
    products = Product.objects.all()
    paginator = Paginator(products, 6)

    page = request.GET.get('page')
    products = paginator.get_page(page)

    context = {
        'categories': categories,
        'products': products,
        'cart': cart,
    }
    return render(request, 'main_page.html', context)

def product_view(request, product_slug):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    product = Product.objects.get(slug=product_slug)
    #categories = Category.objects.all()
    context = {
        #'categories': categories,
        'product': product,
        'cart': cart
    }
    return render(request, 'product1.html', context)

def category_view(request, category_slug):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    category = Category.objects.get(slug=category_slug)
    products_in_cat = Product.objects.filter(category=category)
#    categories = Category.objects.all()
    context = {
        'category': category,
        'products_in_cat': products_in_cat
        #'categories': categories
    }
    return render(request, 'category1.html', context)

def cart_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    categories = Category.objects.all()
    context = {
        'cart': cart,
        'categories': categories
    }
    return render(request, 'cart1.html', context)

def add_item_cart(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    product_slug = request.GET.get('product_slug')
    product = Product.objects.get(slug=product_slug)
    cart.add_cart_item_to_cart(product_slug)
    cart_total_price = 0.00
    for item in cart.items.all():
        cart_total_price += float(item.total_item)
    cart.total_cart = cart_total_price
    cart.save()
    return JsonResponse({'total_cart': cart.items.count(), 'cart_total_price': cart.total_cart})

def remove_item_cart(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    product_slug = request.GET.get('product_slug')
    prod = Product.objects.get(slug=product_slug)
    cart.remove_cart_item_from_cart(product_slug)
    cart_total_price = 0.00
    for item in cart.items.all():
        cart_total_price += float(item.total_item)
    cart.total_cart = cart_total_price
    cart.save()
    return JsonResponse({'total_cart': cart.items.count(), 'cart_total_price': cart.total_cart})

def change_item_count(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    count = request.GET.get('count')
    item_id = request.GET.get('item_id')
    cart.change_count(count, item_id)
    cart_item = CartItem.objects.get(id=int(item_id))
    return JsonResponse({'total_cart': cart.items.count(),
     'total_item': cart_item.total_item, 'cart_total_price': cart.total_cart})


def make_discount(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    coupon = request.GET.get('coupon')
    cart.make_discount(coupon)
    return JsonResponse({'cart_total_price': cart.total_cart})

def checkout_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    categories = Category.objects.all()
    context = {
        'cart': cart,
        'categories': categories
    }
    return render(request, 'checkout.html', context)

def order_create_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    categories = Category.objects.all()
    form = OrderForm(request.POST or None)
    context = {
        'form': form,
        'cart': cart,
        'categories': categories
    }
    return render(request, 'order.html', context)

def make_order_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    form = OrderForm(request.POST or None)
    categories = Category.objects.all()
    if form.is_valid():
        name = form.cleaned_data['name']
        last_name = form.cleaned_data['last_name']
        phone = form.cleaned_data['phone']
        buying_type = form.cleaned_data['buying_type']
        address = form.cleaned_data['address']
        comments = form.cleaned_data['comments']
        new_order = Order.objects.create(
                user = request.user,
                items = cart,
                total = cart.total_cart,
                first_name = name,
                last_name = last_name,
                phone = phone,
                address = address,
                buying_type = buying_type,
                comments = comments
            )

        del request.session['cart_id']
        del request.session['total']
        return HttpResponseRedirect(reverse('thank_you'))
    return render(request, 'order.html', {'categories': categories})

def account_view(request):
    order = Order.objects.filter(user=request.user).order_by('-id')
    categories = Category.objects.all()
    context = {
        'order': order,
        'categories': categories
    }
    return render(request, 'account.html', context)

def registration_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    form = RegistrationForm(request.POST or None)
    categories = Category.objects.all()
    if form.is_valid():
        new_user = form.save(commit=False)
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['password']
        email = form.cleaned_data['email']
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        new_user.first_name = first_name
        new_user.last_name = last_name
        new_user.email = email
        new_user.username = username
        new_user.set_password(password)
        new_user.save()
        aunth_user = authenticate(username=username, password=password)
        if aunth_user:
            login(request, aunth_user)
            return HttpResponseRedirect(reverse('main_page'))
    context = {
        'form': form,
        'categories': categories
    }
    return render(request, 'registration.html', context)


def login_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    form = LoginForm(request.POST or None)
    #categories = Category.objects.all()
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        # raise ValueError('A very specific bad thing happened.')
        aunth_user = authenticate(username=username, password=password)
        if aunth_user:
            login(request, aunth_user)
            return HttpResponseRedirect(reverse('main_page'))
    context = {
        'form': form,
        # 'categories': categories
    }
    return render(request, 'login.html', context)
