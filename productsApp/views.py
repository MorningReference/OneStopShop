from django.shortcuts import render, HttpResponse, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import *
from django.db.models import Sum
from django.views.decorators.csrf import csrf_exempt
import stripe
import json
from django.http import JsonResponse


def index(request):
    if 'user_id' not in request.session:
        context = {
            'user': User.objects.filter(id=2)[0],
            'all_categories': Category.objects.all()[:6],
            'categories_all': Category.objects.all(),
            "products_first": Product.objects.all()[43:46],
            "products_second": Product.objects.all()[47:50]
        }
        return render(request, 'index.html', context)
    context = {
        "user": User.objects.filter(id=request.session['user_id'])[0],
        "products": Product.objects.all()[7:13],
        'all_categories': Category.objects.all()[:6],
        'categories_all': Category.objects.all(),
        "products_first": Product.objects.all()[43:46],
        "products_second": Product.objects.all()[47:50]
    }
    return render(request, "index.html", context)


def products(request, categoryName=''):
    products_list = Product.objects.filter(category__name=categoryName).all()
    paginator = Paginator(products_list, 6)

    page_number = request.GET.get('page', 1)
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    if(len(categoryName) != 0):
        context = {
            'products': page_obj,
            "user": User.objects.filter(id=request.session['user_id'])[0],
            'categories': Category.objects.all(),
            # 'page_obj': page_obj
        }
        return render(request, 'productsListing.html', context)
    else:
        context = {
            'products': Product.objects.all(),
            "user": User.objects.filter(id=request.session['user_id'])[0],
            'categories': Category.objects.all(),
        }
        # change the name of the html to something different
        return render(request, 'productsListing.html', context)


def singleProduct(request, productId=1):
    product = Product.objects.filter(id=productId)[0]
    context = {
        "user": User.objects.filter(id=request.session['user_id'])[0],
        "product": product,
        'similar_products': Product.objects.filter(category=Category.objects.filter(products=product)[0])[:7],
    }
    return render(request, "productPage.html", context)

# def showShoppingCart(request):#add userId
#     context = {
#         # "User": User.objects.filter(id=userID),
#         # "Product": Product.objects.all()
#     }
#     return render(request, "shoppingCart.html", context)

# Shopping Cart


def addToCart(request, productId):  # changed ShoppingCart_id to productId
    # ShoppingCart.objects.get(id=ShoppingCart_id).products.add(Product.objects.get(id=request.POST['product_id']))
    user = User.objects.filter(id=request.session['user_id'])[0]
    shoppingCart = ShoppingCart.objects.filter(user=user).first()
    if not shoppingCart:
        ShoppingCart.objects.create(user=user)
    # quantity = int(request.POST['quantity'])
    # for i in range(quantity):
    ShoppingCart.objects.filter(user=user)[0].products.add(
        Product.objects.filter(id=productId)[0])
    # ajax action? so it doesn't make the user navigate away form the page every time they add a new item
    return redirect(f'/user/{user.id}/shoppingCart')


def shoppingCart(request, userId):  # changed user_id to userId
    context = {
        'products_in_cart': Product.objects.filter(shoppingCart__user__id=request.session['user_id']),
        'user': User.objects.filter(id=userId)[0],
    }
    return render(request, "shopping_cart.html", context)


# changed product_id to productId and added userId
def deleteCartItem(request, userId, productId):
    # to_delete=ShoppingCart.objects.get(id=product_id)
    # to_delete.delete()
    product_to_remove = Product.objects.filter(id=productId)[0]
    ShoppingCart.objects.filter(user=User.objects.filter(id=userId)[0])[
        0].products.remove(product_to_remove)
    return redirect(f'/user/{userId}/shoppingCart')


def showPayment(request, userId=1):  # productId
    context = {
        "User": User.objects.get(id=userId),
        "products": Product.objects.filter(shoppingCart__user__id=userId).all()
    }
    # render payment page with all of the items from shopping cart
    return render(request, "payment.html", context)


@csrf_exempt
def createPayment(request, userId):
    user = User.objects.filter(id=userId)[0]
    cart = Product.objects.filter(shoppingCart__user=user).all()
    total = cart.aggregate(Sum('price'))['price__sum']
    total *= 100
    stripe.api_key = 'sk_test_51GuRsoCHa7tWmaIpdwnzJmINZHe72TJ9EysvgL0N1mKY48NWPJRvwhh2z6VIv3hwjnTzM1Ij8aJISfWOWQXgpY2O007hFB1Eax'

    if request.method == "POST":
        data = json.loads(request.body)
        intent = stripe.PaymentIntent.create(amount=total, currency='usd', metadata={
            'integration_check': 'accept_a_payment'},)
        try:
            return JsonResponse({'publishableKey': 'pk_test_51GuRsoCHa7tWmaIpCliv1INqTrABvAiPwQkef1fZ2ZegWptiBWPJf34SrGVxyf3NMqO1ZrINg7E1azIaUNiqQ8KP00jSPXRv0P', 'clientSecret': intent.client_secret})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=403)


def paymentComplete(request):
    if request.method == "POST":
        data = json.loads(request.POST.get("payload"))
        if data["status"] == "succeeded":
            # save purchase here/ setup email confirmation
            return render(request, "receipt.html")


def processPayment(request, userId):
    # errors = User.objects.tripValidator(request.POST)

    # if len(errors) > 0:
    #     for key, value in errors.items():
    #         messages.error(request, value, extra_tags=key)
    #     return redirect(f"/dashboard/trip/new")
    user = User.objects.filter(id=userId)[0]
    cart = Product.objects.filter(shoppingCart__user=user).all()
    order = Order.objects.create(user=user)
    for product in cart:
        order.products.add(product)
    if request.POST['check'] == 'sameAsShipping':
        ship = ShippingInfo.objects.create(
            first_name=request.POST['shipping_firstName'],
            last_name=request.POST['shipping_lastName'],
            address=request.POST['shipping_address'],
            address2=request.POST['shipping_address2'],
            city=request.POST['shipping_city'],
            state=request.POST['shipping_state'],
            zipcode=request.POST['shipping_zipcode'],
            user=user
        )
        process = BillingInfo.objects.create(
            first_name=request.POST['shipping_firstName'],
            last_name=request.POST['shipping_lastName'],
            address=request.POST['shipping_address'],
            address2=request.POST['shipping_address2'],
            city=request.POST['shipping_city'],
            state=request.POST['shipping_state'],
            zipcode=request.POST['shipping_zipcode'],
        )

        pay = PaymentInfo.objects.create(
            card_number=request.POST['credit_card'],
            expiration_date=request.POST['expDate'],
            security_number=request.POST['security_code'],
            user=user,
            billingInfo=process
        )

    else:
        ship = ShippingInfo.objects.create(
            first_name=request.POST['shipping_firstName'],
            last_name=request.POST['shipping_lastName'],
            address=request.POST['shipping_address'],
            address2=request.POST['shipping_address2'],
            city=request.POST['shipping_city'],
            state=request.POST['shipping_state'],
            zipcode=request.POST['shipping_zipcode'],
            user=user
        )
        process = BillingInfo.objects.create(
            first_name=request.POST['billing_firstName'],
            last_name=request.POST['billing_lastName'],
            address=request.POST['billing_address'],
            address2=request.POST['billing_address2'],
            city=request.POST['billing_city'],
            state=request.POST['billing_state'],
            zipcode=request.POST['billing_zipcode']

        )
        pay = PaymentInfo.objects.create(
            card_number=request.POST['credit_card'],
            expiration_date=request.POST['expDate'],
            security_number=request.POST['security_code'],
            user=user,
            billingInfo=process
        )
    return redirect("/receipt")


# Wish List
def wishList(request, userId=1):
    # include context dictionary to pass the wish list object linked to the user
    context = {
        'products_in_wish': Product.objects.filter(wishList__user__id=request.session['user_id']),
        'user': User.objects.filter(id=userId)[0],
    }
    return render(request, "wish_list.html", context)


def addWishItem(request, productId):  # changed wish_id to userId
    # WishList.objects.get(id=wishList_id).products.add(Product.objects.get(id=request.POST['product_id']))
    user = User.objects.filter(id=request.session['user_id'])[0]
    wishList = WishList.objects.filter(user=user).first()
    if not wishList:
        WishList.objects.create(user=user)
    # quantity = int(request.POST['quantity'])
    # for i in range(quantity):
    WishList.objects.filter(user=user)[0].products.add(
        Product.objects.filter(id=productId)[0])
    return redirect('/wishlist')


# changed product_id to productId and added userId
def deleteWishItem(request, userId, productId):
    to_delete = WishList.objects.get(id=product_id)
    to_delete.delete()
    return redirect('/wishlist')


# replace ShoppingCart_id with userId and productId
def addWishToCart(request, userId, productId):
    # ShoppingCart.objects.get(id=ShoppingCart_id).products.add(Product.objects.get(id=request.POST['product_id']))
    ShoppingCart.objects.filter(user=User.objects.filter(id=userId)[0])[
        0].products.add(Product.objects.filter(id=productId)[0])
    # ajax action? so it doesn't make the user navigate away form the page every time they add a new item
    return redirect(f'/user/{{userId}}/wishlist')
    # this cannot be right...

# Receipt


def showReceipt(request):
    # if user is authenticated
    return render(request, 'receipt.html')


def showOrders(request, userId=1):
    user = User.objects.filter(id=userId)[0]
    context = {
        'user': user,
        'all_the_orders': Order.objects.filter(user=user).all()
    }
    return render(request, 'orders.html', context)


def singleOrder(request, userId, orderId=1):
    user = User.objects.filter(id=userId)[0]
    context = {
        'user': user,
        'order': Order.objects.filter(id=orderId),
    }
    return render(request, 'orderPage.html', context)
