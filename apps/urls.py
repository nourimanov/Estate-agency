from django.core import signing
from django.urls import path
from apps.views import about, agent_single, agents_grid, blog_grid, blog_single, contact, index, property_grid, \
    property_single, signup, signin, add_category, add_blog, logout, logout_view

urlpatterns = [
    path('', index, name='index'),
    path('agent_single/<pk>', agent_single, name='agent_single'),
    path('agents_grid/', agents_grid, name='agents_grid'),
    path('blog_grid/', blog_grid, name='blog_grid'),
    path('blog_single/<pk>/', blog_single, name='blog_single'),
    path('contact/', contact, name='contact'),
    path('about/', about, name='about'),
    path('property_grid/', property_grid, name='property_grid'),
    path('property_single/<pk>/', property_single, name='property_single'),
    path('signup/', signup, name='signup'),
    path('signin/', signin, name='signin'),
    path('logout/', logout_view, name='logout'),
    path('add_category/', add_category, name='category'),
    path('add_blog/', add_blog, name='blog'),
]

