from django.shortcuts import render
from django.http import JsonResponse
import json
import random
import datetime
from .models import * 
from .utils import cookieCart, cartData, guestOrder
from django.core.paginator import Paginator 

def store(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	categories = Category.objects.all()
	prods = random.sample(list(Product.objects.all()), 8)
	context = {'categories': categories, 'products':prods, 'cartItems':cartItems, 'items':items, 'order':order}
	return render(request, 'store/store.html', context)


def cart(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/cart.html', context)

def checkout(request):
	data = cartData(request)
	
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/checkout.html', context)

# def updateItem(request):

# 	data = json.loads(request.body)
# 	productId = data['productId']
# 	action = data['action']
# 	print('Action:', action)
# 	print('Product:', productId)

# 	customer = request.user.customer
# 	product = Product.objects.get(id=productId)
# 	order, created = Order.objects.get_or_create(customer=customer, complete=False)

# 	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

# 	if action == 'add':
# 		orderItem.quantity = (orderItem.quantity + 1)
# 	elif action == 'remove':
# 		orderItem.quantity = (orderItem.quantity - 1)

# 	orderItem.save()

# 	if orderItem.quantity <= 0 or action == 'delete':
# 		orderItem.delete()
	

# 	return JsonResponse('Item was added', safe=False)

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	
	customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		country=data['shipping']['country'],
		zipcode=data['shipping']['zipcode'],
		)
	

	return JsonResponse('Payment submitted..', safe=False)

def product(request, productId):
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	
	product = Product.objects.get(id=productId)
	images = ProductImage.objects.filter(product=product)
	num = 0
	if len(Product.objects.filter(category=product.category)) > 2:
		num = int(len(Product.objects.filter(category=product.category))/2)
	relatedProds = random.sample(list(Product.objects.filter(category=product.category)), num)
	return render(request, 'store/product.html', {'title': product.name ,'product': product, 'images': images, 'relatedProds': relatedProds, 'cartItems':cartItems,'order':order, 'items': items})

def catalog(request):
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	itemsINcart = data['items']

	categories = Category.objects.all()
	items = 0
	for category in categories:
		for subcategory in category.subcategory_set.all():
			items += len(subcategory.product_set.all())
	return render(request, 'store/catalog.html', {'title': 'Catalog','categories': categories, 'TotalItems': items, 'cartItems':cartItems,'order':order, 'items': itemsINcart})

def category(request, categoryId):
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	itemsINcart = data['items']

	category = Category.objects.get(id=categoryId)
	items = 0
	catProds = []
	
	for subcategory in category.subcategory_set.all():
		items += len(subcategory.product_set.all())
		catProds.append(Product.objects.filter(category=subcategory.id)) 
	
	prods = []
	for prodsubcat in catProds:
		for prod in prodsubcat:
			prods.append(prod)
	paginator = Paginator(prods, per_page=3)
	page_number = request.GET.get('page', 1)
	page = paginator.page(page_number)
	page_obj = paginator.get_page(page_number)
	return render(request, 'store/category.html', {'title':category.name ,'category': category ,'catItems': page_obj.object_list, 'TotalItems': items, 'cartItems':cartItems,'order':order, 'items': itemsINcart, 'paginator': paginator, 'page_number': int(page_number), 'page': page})

def subcategory(request, subcategoryId):
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	itemsINcart = data['items']

	subcategory = Subcategory.objects.get(id=subcategoryId)
	items = len(subcategory.product_set.all())
	

	paginator = Paginator(Product.objects.filter(category=subcategory.id), per_page=3)
	page_number = request.GET.get('page', 1)
	page = paginator.page(page_number)
	page_obj = paginator.get_page(page_number)
	return render(request, 'store/subcategory.html', {'title': subcategory.name,'subcategory': subcategory , 'subcatItems': page_obj.object_list, 'TotalItems': items, 'cartItems':cartItems,'order':order, 'items': itemsINcart, 'paginator': paginator, 'page_number': int(page_number), 'page': page})


def search(request):
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	query = request.GET.get('query')
	products = Product.objects.filter(name__icontains=query)
	paginator = Paginator(products, per_page=8)
	page_number = request.GET.get('page', 1)
	page = paginator.page(page_number)
	page_obj = paginator.get_page(page_number)
	return render(request, 'store/search_result.html', {'title':'Search Result','cartItems':cartItems,'order':order, 'items': items, 'result': products, 'paginator': paginator, 'page_number': int(page_number), 'page': page})

def priceFilter(request, subcategoryId):
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	products = Product.objects.filter(category=subcategoryId)
	min = 0
	max = 0
	if request.GET.get('min'):
		min = request.GET.get('min')
	if request.GET.get('max'):
		max = request.GET.get('max')
	cleanedProducts = []
	for prod in products:
		if int(prod.price) in range(int(min), int(max)+1):
			cleanedProducts.append(prod)
	paginator = Paginator(cleanedProducts, per_page=8)
	page_number = request.GET.get('page', 1)
	page = paginator.page(page_number)
	page_obj = paginator.get_page(page_number)
	return render(request, 'store/search_result.html', {'title':'Result','cartItems':cartItems,'order':order, 'items': items, 'result': cleanedProducts, 'paginator': paginator, 'page_number': int(page_number), 'page': page})


def about(request):
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	return render(request, 'store/about.html', {'title':'About','cartItems':cartItems,'order':order, 'items': items})

    

def contacts(request):
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	return render(request, 'store/contacts.html', {'title':'Contacts', 'cartItems':cartItems,'order':order, 'items': items}) 

def processContact(request):
	data = json.loads(request.body)
	ContactMessage.objects.create(
		name= data['form']['name'],
		email= data['form']['email'],
		topic= data['form']['topic'],
		message= data['form']['message'],
	)
	return JsonResponse('Message saved..', safe=False)

def fqa(request):
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	return render(request, 'store/fqa.html', {'title': "FQA", 'cartItems':cartItems,'order':order, 'items': items})
