from django.urls import path

from . import views


urlpatterns = [
	#Leave as empty string for base url
	path('', views.store, name="home"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	#path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),
	path('process_contact/', views.processContact, name="process_contact"),
	path('product/<int:productId>', views.product, name="store-product"),
	path('catalog/', views.catalog, name='store-catalog'),
	path('category/<int:categoryId>', views.category, name='category'),
	path('subcategory/<int:subcategoryId>', views.subcategory, name='subcategory'),
	path('search_result/', views.search, name='store-search'),
	path('pricefilter/<int:subcategoryId>', views.priceFilter, name='store-filter'),
	path('contacts/', views.contacts, name='store-contacts'),
    path('about/', views.about, name='store-about'),
    path('fqa/', views.fqa, name='store-fqa'),
]