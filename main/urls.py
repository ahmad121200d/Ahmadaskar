from django.urls import path
from . import views

# هذا الملف يحتوي على أنماط الروابط (URL Patterns) الخاصة بتطبيق 'main'.
# عندما يأتي طلب إلى رابط معين، يبحث Django في هذه القائمة من الأعلى إلى الأسفل.
# أول نمط يتطابق مع الرابط المطلوب هو الذي يتم استخدامه.

urlpatterns = [
    # الرابط الفارغ ('') يعني الصفحة الرئيسية للموقع.
    # views.home هو دالة الـ View التي سيتم استدعاؤها.
    # name='home' هو اسم فريد لهذا الرابط، يمكننا استخدامه في القوالب والـ Views لإعادة التوجيه بدلاً من كتابة الرابط كاملاً.
    path('', views.home, name='home'),

    # الروابط الخاصة بالمراكز التجارية (Malls)
    path('malls/', views.mall_list, name='mall_list'),
    path('malls/add/', views.add_mall, name='add_mall'),
    # <int:mall_id> هو جزء متغير من الرابط. int تعني أنه يجب أن يكون رقماً صحيحاً.
    # سيتم تمرير هذا الرقم كمعامل (parameter) اسمه mall_id إلى دالة الـ view.
    path('malls/<int:mall_id>/edit/', views.edit_mall, name='edit_mall'),
    path('malls/<int:mall_id>/delete/', views.delete_mall, name='delete_mall'),
    
    # الروابط الخاصة بالمنتجات (Products)، وهي مرتبطة بمركز تجاري معين
    path('malls/<int:mall_id>/products/', views.mall_products, name='mall_products'),
    path('malls/<int:mall_id>/products/add/', views.add_product, name='add_product'),
    path('malls/<int:mall_id>/products/<int:product_id>/edit/', views.edit_product, name='edit_product'),
    path('malls/<int:mall_id>/products/<int:product_id>/delete/', views.delete_product, name='delete_product'),

    # رابط صفحة الملف الشخصي
    path('profile/', views.profile_view, name='profile'),
    
    # روابط المصادقة (Authentication)
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # رابط خاص بواجهة برمجة التطبيقات (API) لتسجيل الدخول
    path('api/login/', views.LoginAPIView.as_view(), name='api_login'),
] 