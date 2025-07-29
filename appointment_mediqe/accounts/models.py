from django.db import models
from django.db import models

class User(models.Model):
    # شناسه یکتا برای هر کاربر، از نوع UUID
    id = models.UUIDField(primary_key=True, editable=False)
    # نام کاربری
    username = models.CharField(max_length=150)
    # ایمیل کاربر، باید یکتا باشد
    email = models.EmailField(unique=True)
    # رمز عبور کاربر
    password = models.CharField(max_length=128)
    
    # نقش کاربر، با گزینه‌های مختلف
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Doctor', 'Doctor'),
        ('Patient', 'Patient'),
        ('Nurse', 'Nurse'),
        ('Receptionist', 'Receptionist'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    
    # نام و نام خانوادگی کاربر
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    # تاریخ تولد کاربر
    date_of_birth = models.DateField()
    
    # جنسیت، با گزینه‌های مختلف
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    
    # شماره تماس
    phone = models.CharField(max_length=20)
    # آدرس
    address = models.TextField()
    # تصویر پروفایل (آواتار)، آپلود در پوشه 'avatars/'
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    
    # وضعیت فعال بودن حساب کاربر
    is_active = models.BooleanField(default=True)
    # تایید شدن حساب کاربر
    is_verified = models.BooleanField(default=False)
    # تاریخ ساخت حساب
    created_at = models.DateTimeField(auto_now_add=True)
    
    # اطلاعات اضافی، در قالب JSON
    extra_info = models.JSONField(null=True, blank=True)

    # رشته‌ای که نمایش می‌دهد شیء این کلاس چه باشد
    def __str__(self):
        return self.username


class UserProfile(models.Model):
    # رابطه یکی به یکی با مدل User
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # شماره بیمه
    insurance_number = models.CharField(max_length=50)
    # نام شرکت بیمه
    insurance_company = models.CharField(max_length=100)
    # گروه خونی
    blood_type = models.CharField(max_length=3)
    
    # شرایط مزمن پزشکی
    chronic_conditions = models.TextField()
    # شماره مجوز
    license_number = models.CharField(max_length=50)
    # تخصص پزشک یا پرستار
    specialty = models.CharField(max_length=50)
    # بیوگرافی یا توضیحات فرد
    bio = models.TextField()
    
    # سال‌های تجربه کاری
    years_experience = models.IntegerField()
    # امتیاز یا رتبه‌بندی
    rating = models.FloatField()
    # وضعیت تایید پروفایل
    verified = models.BooleanField(default=False)

    # نمایش نام کاربر در قالب رشته
    def __str__(self):
        return f"{self.user.username} Profile"


class AuditLog(models.Model):
    # شناسه یکتا، از نوع UUID
    id = models.UUIDField(primary_key=True, editable=False)
    # کاربری که عملیات انجام داده
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    # نوع عمل انجام شده
    action = models.CharField(max_length=50)
    # هدف عمل یا موضوع آن
    target = models.CharField(max_length=100)
    # تاریخ و زمان انجام عملیات
    timestamp = models.DateTimeField(auto_now_add=True)
    # آدرس آی‌پی کاربر
    ip_address = models.CharField(max_length=45)
    # جزئیات بیشتر درباره عملیات
    details = models.TextField()

    # رشته‌ای نمایش‌دهنده عملیات
    def __str__(self):
        return f"{self.action} by {self.user}"


class Notification(models.Model):
    # شناسه یکتا، از نوع UUID
    id = models.UUIDField(primary_key=True, editable=False)
    # کاربر هدف نوتیفیکیشن
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    # نوع نوتیفیکیشن
    type = models.CharField(max_length=50)
    # عنوان نوتیفیکیشن
    title = models.CharField(max_length=100)
    # محتوای نوتیفیکیشن
    content = models.CharField(max_length=255)
    # وضعیت خوانده یا نخوانده بودن
    is_read = models.BooleanField(default=False)
    # تاریخ ساخت نوتیفیکیشن
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} → {self.user}"
    