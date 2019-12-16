""" URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls import url, include
from django.urls import reverse_lazy
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from django.conf import settings
from myapp.views import main_page, product_view, category_view, cart_view, add_item_cart, remove_item_cart, change_item_count, checkout_view, order_create_view, make_order_view, account_view, registration_view, login_view, make_discount

urlpatterns = [

    url(r'^$', main_page, name='main_page'),
    url(r'^category/(?P<category_slug>[-\w]+)/$', category_view, name='category_detail'),
    url(r'^product/(?P<product_slug>[-\w]+)/$', product_view, name='product_detail'),
    url(r'^add_item_cart/$', add_item_cart, name='add_item_cart'),
    url(r'^remove_item_cart/$', remove_item_cart, name='remove_item_cart'),
    url(r'^change_item_count/$', change_item_count, name='change_item_count'),
    url(r'^make_discount/$', make_discount, name='make_discount'),
    url(r'^checkout_view/$', checkout_view, name='checkout_view'),
    url(r'^order/$', order_create_view, name='create_order'),
    url(r'^make_order/$', make_order_view, name='make_order'),
    url(r'^account/$', account_view, name='account'),
    url(r'^thank_you/$', TemplateView.as_view(template_name='thank_you.html'), name='thank_you'),
    url(r'^registration/$', registration_view, name='registration'),
    url(r'^login/$', login_view, name='login'),
    url(r'^logout/$', LogoutView.as_view(next_page=reverse_lazy('main_page')), name='logout'),
    url(r'cart/$', cart_view, name='cart')
]
