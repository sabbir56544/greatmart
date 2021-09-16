from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, redirect, render
from .models import Product, Category, Cart, CartItem, Variation
from django.http.response import HttpResponse, JsonResponse

from django.db.models import Q
#paginator
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

def home(request):
    categories = Category.objects.all()
    products = Product.objects.filter(is_stock=True)
    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'index.html', context)



def store(request, category_slug=None):
    categories = None
    products = None 

    category = Category.objects.all()
    
    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_stock=True)

        #paginator
        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        pagged_products = paginator.get_page(page)
        products_count = products.count()
    else:
        products = Product.objects.filter(is_stock=True)

        #paginator
        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        pagged_products = paginator.get_page(page)
        products_count = products.count()

    context = {
        'products': pagged_products,
        'products_count': products_count,
        'categories': category,
    }
    return render(request, 'store.html', context)



def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    except Exception as e:
        raise e

    context = {
        'single_product': single_product,
        'in_cart': in_cart,
    }        
    return render(request, 'product_detail.html', context)



def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart



def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    # product variation
    product_variation = []
    if request.method == 'POST':
        for item in request.POST:
            key = item
            value = request.POST[key]

            try:
                variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                product_variation.append(variation)
            except:
                pass 
                
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request)) # get the cart using the cart_id present in the session
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id = _cart_id(request))
        cart.save()

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)

        # variation
        if len(product_variation) > 0:
            cart_item.variations.clear()
            for item in product_variation:
                cart_item.variations.add(item) #end variation
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)

        #variation
        if len(product_variation) > 0:
            cart_item.variations.clear()
            for item in product_variation:
                cart_item.variations.add(item) #end variation
        cart_item.save()
    return redirect('cart_view')        


def cart_view(request, total=0, quantity=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id = _cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total) / 100
        grand_total = total + tax    
    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax' : tax,
        'grand_total': grand_total,
    }   

    return render(request, 'cart_view.html', context)



def remove_cart(request, product_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity >= 0:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart_view')


def remove_cart_item(request, product_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart_view')

# search product


def search_product(request):
    if request.method == 'POST':
        search_keyword = request.POST['search_keyword']
        products = Product.objects.filter(Q(product_name__contains=search_keyword) | Q(category__category_name__contains=search_keyword))
        product_count = products.count()
        category = Category.objects.all()
        return render(request, 'search.html', {'products': products, 'search_key': search_keyword, 'categories': category, 'product_count': product_count})
   


def autosuggest(request):
    query_original = request.GET.get('term')
    queryset = Product.objects.filter(Q(product_name__icontains=query_original) | Q(category__category_name__icontains=query_original))
    mylist = []
    mylist += [x.product_name for x in queryset ]
    return JsonResponse(mylist, safe=False)
