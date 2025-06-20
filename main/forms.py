from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Product, Mall
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

# ملف Forms.py يستخدم لإنشاء نماذج إدخال بيانات يمكن عرضها في صفحات HTML.
# الفائدة الرئيسية هي أنها تقوم بالتحقق من صحة البيانات (Validation) تلقائياً.

# هذا النموذج خاص بتعديل الملف الشخصي للمستخدم.
# إنه لا يرتبط مباشرة بـ ModelForm لأنه يعدل بيانات من موديل User و UserProfile معاً.
class UserProfileForm(forms.ModelForm):
    # تعريف حقول إضافية غير موجودة في موديل UserProfile مباشرة
    username = forms.CharField(max_length=150, required=True, label='اسم المستخدم')
    email = forms.EmailField(required=False, label='البريد الإلكتروني')

    # Meta class يربط النموذج بالموديل ويحدد الحقول التي يجب عرضها
    class Meta:
        model = UserProfile
        fields = ['image', 'phone', 'address']
        labels = {
            'image': '',
            'phone': 'رقم الهاتف',
            'address': 'موقع السكن',
        }
        widgets = {
            # هذا يخفي حقل إدخال الملف الأصلي، لأننا سنقوم بتفعيله عبر النقر على الصورة.
            'image': forms.FileInput(attrs={'style': 'display:none;'})
        }

    # دالة __init__ يتم استدعاؤها عند إنشاء كائن من الكلاس
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # هنا نقوم بإضافة كلاس Bootstrap 'form-control' لكل حقل لتوحيد التصميم
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['phone'].widget.attrs.update({'class': 'form-control'})
        self.fields['address'].widget.attrs.update({'class': 'form-control'})

# ModelForm هو نوع خاص من النماذج يتم إنشاؤه تلقائياً من موديل معين.
class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # جعل حقل الصورة غير إجباري. هذا يمنع ظهور خطأ عند حفظ النموذج بدون تغيير الصورة.
        # كما أنه يزيل مربع "Clear" الذي يظهر بجانب حقل الصورة.
        self.fields['image'].required = False
        
        # إعدادات Crispy Forms
        self.helper = FormHelper()
        # form_tag = False يمنع Crispy من إنشاء وسم <form> بنفسه.
        # هذا مفيد لأننا نتحكم بوسم الفورم يدوياً في القالب (لإضافة id مثلاً).
        self.helper.form_tag = False 
        # disable_csrf = True يمنع Crispy من إضافة {% csrf_token %} لأنه موجود بالفعل في القالب.
        self.helper.disable_csrf = True

    class Meta:
        model = Product
        # تحديد الحقول التي ستظهر في النموذج
        fields = ['name', 'description', 'price', 'image']
        # تحديد النصوص التي ستظهر بجانب كل حقل (Labels)
        labels = {
            'name': 'اسم المنتج',
            'description': 'الوصف',
            'price': 'السعر',
            'image': 'صورة المنتج',
        }

class MallForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False
        
        # نفس إعدادات Crispy Forms كما في نموذج المنتج
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True

    class Meta:
        model = Mall
        fields = ['name', 'working_hours', 'governorate', 'mall_type', 'image']
        labels = {
            'name': 'اسم المركز',
            'working_hours': 'أوقات العمل',
            'governorate': 'المحافظة',
            'mall_type': 'نوع المركز',
            'image': 'صورة المركز',
        } 