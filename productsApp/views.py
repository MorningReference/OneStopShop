from django.shortcuts import render, HttpResponse, redirect
from .models import *
# import requests

def index(request):
    context = {
        "user": User.objects.filter(id=request.session['user_id'])[0],
    }
    return render(request, "index.html", context)

def products(request, categoryName=''):
    if(len(categoryName) != 0):
        # navigate to product page with category selected
        return render(request, 'productsListing.html')
    else:
        # result = requests.get('https://api.printful.com/products').json()['result']
        # print(r)
        # categories = [];
        # productList = [];
        # for item in result:
        #     if item['type'] == 'T-SHIRT':
        #         if item['type_name'] not in categories:
        #             categories.append(item['type_name'])
                # print(item['model'])
                # Product.objects.create(
                #     name = item['model'],
                #     desc = item['description'],
                #     price = 9.99,
                #     image = item['image'],
                #     category = Category.objects.filter(name = item['type_name'])[0]
                # )
        # print('this is the products:', productList)
        # context = {
        #     'product': productList,
        #     'categories': categories,
        # }

        context = {
            'categories': Category.objects.all(),
            'products': Product.objects.all()
        }
        return render(request, 'productsListing.html', context) # change the name of the html to something different


def singleProduct(request, productId):
    product = Product.objects.filter(id = productId)[0]
    context = {
        "user": User.objects.filter(id=request.session['user_id'])[0],
        "product": product,
        'similar_products': Product.objects.filter(category = Category.objects.filter(products = product)[0])[:8],
    }
    return render(request, "productPage.html", context)

# def showShoppingCart(request):#add userId
#     context = {
#         # "User": User.objects.filter(id=userID),
#         # "Product": Product.objects.all()
#     }
#     return render(request, "shoppingCart.html", context)

##Shopping Cart
def addToCart(request, productId): # changed ShoppingCart_id to productId
    # ShoppingCart.objects.get(id=ShoppingCart_id).products.add(Product.objects.get(id=request.POST['product_id']))
    user = User.objects.filter(id = request.session['user_id'])[0]
    shoppingCart = ShoppingCart.objects.filter(user = user)
    if not shoppingCart:
        ShoppingCart.objects.create(user = user)
    ShoppingCart.objects.filter(user = user)[0].products.add(Product.objects.filter(id = productId)[0])
    return redirect(f'/user/{user.id}/shoppingCart') # ajax action? so it doesn't make the user navigate away form the page every time they add a new item

def shoppingCart(request, userId): #changed user_id to userId
    context = {
        'products_in_cart': Product.objects.filter(shoppingCart__user__id = request.session['user_id']),
        'user': User.objects.filter(id = userId),
    }
    return render(request, "shopping_cart.html", context)


def deleteCartItem(request, userId, productId): # changed product_id to productId and added userId
    # to_delete=ShoppingCart.objects.get(id=product_id)
    # to_delete.delete()
    product_to_remove = Product.objects.filter(id = productId)[0]
    ShoppingCart.objects.filter(user = User.objects.filter(id = userId)[0])[0].products.remove(product_to_remove)
    return redirect(f'/user/{{userId}}/shoppingCart')

def showPayment(request, userId): #productId
    context = {
        "User": User.objects.filter(id=userId),
        "Product": Product.objects.filter(id=userId)
    }
    return render(request, "payment.html", context)# render payment page with all of the items from shopping cart

def processPayment(request, userId):
        
    # errors = User.objects.tripValidator(request.POST)
    
    # if len(errors) > 0:
    #     for key, value in errors.items():
    #         messages.error(request, value, extra_tags=key)
    #     return redirect(f"/dashboard/trip/new")
    userid = request.session['user_id']   
    user = User.objects.filter(id = userid)[0]
    pay = ShippingInfo.objects.create(
        userID = user,
        first_name = request.POST['destination'],
        last_name = request.POST['startDate'],
        address = request.POST['endDate'],
        adress2 = request.POST['planTrip'],
        city = request.POST['destination'],
        state = request.POST['startDate'],
        zipcode = request.POST['endDate'],
    )
    return redirect("/dashboard")

    return HttpResponse('process payment') # process the payment and redirect to the receipt page


## Wish List
def wishList(request, userID):
    # include context dictionary to pass the wish list object linked to the user
    return render(request, "wish_list.html")

def addWishItem(request, userId): # changed wish_id to userId
    WishList.objects.get(id=wishList_id).products.add(Product.objects.get(id=request.POST['product_id']))

    return redirect('/wishlist')

def deleteWishItem(request, userId, productId): # changed product_id to productId and added userId
    to_delete=wishList.objects.get(id=product_id)
    to_delete.delete()
    return redirect('/wishlist')

def addWishToCart(request, userId, productId): # replace ShoppingCart_id with userId and productId
    # ShoppingCart.objects.get(id=ShoppingCart_id).products.add(Product.objects.get(id=request.POST['product_id']))
    ShoppingCart.objects.filter(user = User.objects.filter(id = userId)[0])[0].products.add(Product.objects.filter(id = productId)[0])
    return redirect(f'/user/{{userId}}/wishlist') # ajax action? so it doesn't make the user navigate away form the page every time they add a new item
    ##this cannot be right...

##Receipt
def showReceipt(request, order_id):
    context={
        "purchased_items": Order.objects.get(id=order_id)
    }
    return render(request, 'receipt.html')

