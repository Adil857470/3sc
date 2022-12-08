from django.db import models
from django.contrib.auth.models import User
# Create your models here.
STATUS_CHOICES = (
        ('Active', '1'),
        ('In-Active', '0'),
        )

from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
class UsersManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
        email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        scmuser = ScmUser()
        scmuser.email = email
        scmuser.admin = True
        scmuser.save()
        return user
    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
        email,
        password=password,
        )
        user.staff = True
        user.save(using=self._db)
        scmuser = ScmUser()
        scmuser.email = email
        scmuser.staff = True
        scmuser.save()
        return user
    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
        email,
        password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        scmuser = ScmUser()
        scmuser.email = email
        scmuser.staff = True
        scmuser.save()
        return user


class ScmUser(AbstractBaseUser):
   email=models.CharField(primary_key=True,max_length=300)
   active=models.BooleanField(default=True)
   staff=models.BooleanField(default=False)
   admin=models.BooleanField(default=False)
   time_stamp=models.TimeField(auto_now_add=True)
   USERNAME_FIELD='email'
   REQUIRED_FIELDS=[]
   def get_first_name(self):
      return self.email
   def get_short_name(self):
      return self.email
   def __str__(self):
      return self.email
   def has_perm(self,perm,obj=None):
      return True
   def has_module_perms(self,app_label):
      return True
   @property
   def is_staff(self):
      "Is the user a member of staff?"
      return self.staff
   @property
   def is_admin(self):
      "Is the user a admin member?"
      return self.admin
   @property
   def is_active(self):
      "Is the user active?"
      return self.active
   
   object=UsersManager()



class Tenant(models.Model):
    Id = models.IntegerField(primary_key=True)
    Code=models.CharField(max_length=300,null=True,blank=True)
    Name=models.CharField(max_length=300,null=True,blank=True)
    Description=models.TextField()
    CreatedDate= models.DateField(auto_now_add=True)
    CreatedBy=models.ForeignKey(ScmUser,on_delete=models.CASCADE)
    UpdatedDate=models.DateField(auto_now=True,null=True,blank=True)
    UpdatedBy=models.IntegerField(default=None,blank=True,null=True)
    IPAddress = models.CharField(max_length=300,null=True,blank=True)
    Status=models.IntegerField(choices=STATUS_CHOICES)
    def __str__(self):
        return self.name


# class Channel(models.Model):
#     tenant_id = models.ForeignKey(Tenant, on_delete=models.CASCADE)
#     Code=models.CharField(max_length=200,null=True,blank=True)
#     Name=models.CharField(max_length=300,null=True,blank=True)
#     Description=models.TextField()
#     CreatedDate= models.DateField(auto_now_add=True)
#     CreatedBy=models.ForeignKey(User,on_delete=models.CASCADE)
#     UpdatedDate=models.DateField(auto_now=True)
#     UpdatedBy=models.IntegerField(default=None,blank=True,null=True)
#     IPAddress = models.CharField(max_length=50,null=True,blank=True)
#     Status=models.IntegerField(choices=STATUS_CHOICES)
#     def __str__(self):
#         return self.name

# class BU(models.Model):
#     tenant_id = models.ForeignKey(Tenant, on_delete=models.CASCADE)
#     Code=models.CharField(max_length=200,null=True,blank=True)
#     Name=models.CharField(max_length=300,null=True,blank=True)
#     Description=models.TextField()
#     CreatedDate= models.DateField(auto_now_add=True)
#     CreatedBy=models.ForeignKey(User,on_delete=models.CASCADE)
#     UpdatedDate=models.DateField(auto_now=True)
#     UpdatedBy=models.IntegerField(default=None,blank=True,null=True)
#     IPAddress = models.CharField(max_length=50,null=True,blank=True)
#     Status=models.IntegerField(choices=STATUS_CHOICES)
#     channelid=models.ForeignKey(Channel, on_delete=models.CASCADE)
#     def __str__(self):
#         return self.name


# class Division(models.Model):
#     tenant_id = models.ForeignKey(Tenant, on_delete=models.CASCADE)
#     Code=models.CharField(max_length=200,null=True,blank=True)
#     Name=models.CharField(max_length=300,null=True,blank=True)
#     Description=models.TextField()
#     CreatedDate= models.DateField(auto_now_add=True)
#     CreatedBy=models.ForeignKey(User,on_delete=models.CASCADE,primary_key=True)
#     UpdatedDate=models.DateField(auto_now=True)
#     UpdatedBy=models.IntegerField(default=None,blank=True,null=True)
#     Status=models.IntegerField(choices=STATUS_CHOICES)
#     IPAddress = models.CharField(max_length=50,null=True,blank=True)
#     def __str__(self):
#         return self.name


# class Category(models.Model):
#     tenant_id = models.ForeignKey(Tenant, on_delete=models.CASCADE)
#     Code=models.CharField(max_length=200,null=True,blank=True)
#     Name=models.CharField(max_length=300,null=True,blank=True)
#     Description=models.TextField()
#     CreatedDate= models.DateField(auto_now_add=True)
#     CreatedBy=models.ForeignKey(User,on_delete=models.CASCADE,primary_key=True)
#     UpdatedDate=models.DateField(auto_now=True)
#     UpdatedBy=models.IntegerField(default=None,blank=True,null=True)
#     Status=models.IntegerField(choices=STATUS_CHOICES)
#     IPAddress = models.CharField(max_length=50,null=True,blank=True)
#     def __str__(self):
#         return self.name

# class Brand(models.Model):
#     tenant_id = models.ForeignKey(Tenant, on_delete=models.CASCADE)
#     Code=models.CharField(max_length=200,null=True,blank=True)
#     Name=models.CharField(max_length=300,null=True,blank=True)
#     Description=models.TextField()
#     CreatedDate= models.DateField(auto_now_add=True)
#     CreatedBy=models.ForeignKey(User,on_delete=models.CASCADE)
#     UpdatedDate=models.DateField(auto_now=True)
#     UpdatedBy=models.IntegerField(default=None,blank=True,null=True)
#     Status=models.IntegerField(choices=STATUS_CHOICES)
#     IPAddress = models.CharField(max_length=50,null=True,blank=True)
#     def __str__(self):
#         return self.name


# class tblForecastDtl(models.Model):
#     forecastid=models.PositiveIntegerField()
#     productid=models.PositiveIntegerField()
#     compid=models.PositiveIntegerField()
#     salesmonth=models.DateField()
#     salesyear=models.DateField()
#     salesdate=models.DateField()
#     statsqty=models.CharField(max_length=200,null=True,blank=True)
#     oprtnqty=models.CharField(max_length=250)
#     asp=models.CharField(max_length=250)
#     abc=models.CharField(max_length=200,null=True,blank=True)
#     mo_qty_3sc=models.CharField(max_length=250)
#     m1_qty_3sc=models.CharField(max_length=250)
#     def __str__(self):
#         return self.forecastid



# class SalesOrder_Exim_SFTP(models.Model):
#     order_no=models.PositiveIntegerField()
#     order_date=models.DateField()
#     pick_slip_no=models.PositiveIntegerField()
#     shipper_exporter_Name=models.CharField(max_length=300,null=True,blank=True)
#     shipper_exporter_address=models.CharField(max_length=600,null=True,blank=True)
#     consignee_Name=models.CharField(max_length=300,null=True,blank=True)
#     consignee_address=models.CharField(max_length=600,null=True,blank=True)
#     warehouse_Code=models.PositiveIntegerField()
#     warehouse_Name=models.CharField(max_length=400,null=True,blank=True)
#     warehouse_address=models.CharField(max_length=600,null=True,blank=True)
#     bill_to_Name=models.CharField(max_length=300,null=True,blank=True)
#     def __str__(self):
#         return self.order_no

# class Branch(models.Model):
#     tenant_id = models.ForeignKey(Tenant, on_delete=models.CASCADE)
#     Code=models.CharField(max_length=200,null=True,blank=True)
#     Name=models.CharField(max_length=300,null=True,blank=True)
#     Description=models.TextField()
#     UOM = models.CharField(max_length=100,null=True,blank=True)
#     category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
#     division_id = models.ForeignKey(Division, on_delete=models.CASCADE)
#     brand_id = models.ForeignKey(Brand, on_delete=models.CASCADE)
#     Status=models.IntegerField(choices=STATUS_CHOICES)
#     lead_time = models.CharField(max_length=100,null=True,blank=True)
#     CreatedDate= models.DateField(auto_now_add=True)
#     CreatedBy=models.ForeignKey(User,on_delete=models.CASCADE)
#     UpdatedDate=models.DateField(auto_now=True)
#     UpdatedBy=models.IntegerField(default=None,blank=True,null=True)
#     IPAddress = models.CharField(max_length=50,null=True,blank=True)
#     def __str__(self):
#         return self.name

# class SKU_SNP(models.Model):
#     tenant_id = models.ForeignKey(Tenant, on_delete=models.CASCADE)
#     bu_id = models.ForeignKey(BU, on_delete=models.CASCADE)
#     Code=models.CharField(max_length=200,null=True,blank=True)
#     Name=models.CharField(max_length=300,null=True,blank=True)
#     Description=models.TextField()
#     branch_type = models.CharField(max_length=100,null=True,blank=True)
#     total_volume = models.CharField(max_length=100,null=True,blank=True)
#     total_area = models.CharField(max_length=100,null=True,blank=True)
#     operating_hours = models.CharField(max_length=100,null=True,blank=True)
#     operting_days = models.CharField(max_length=100,null=True,blank=True)
#     operating_times = models.CharField(max_length=100,null=True,blank=True)
#     uploading_times = models.CharField(max_length=100,null=True,blank=True)
#     CreatedDate= models.DateField(auto_now_add=True)
#     CreatedBy=models.ForeignKey(User,on_delete=models.CASCADE)
#     UpdatedDate=models.DateField(auto_now=True)
#     UpdatedBy=models.IntegerField(default=None,blank=True,null=True)
#     Status=models.IntegerField(choices=STATUS_CHOICES)
#     IPAddress = models.CharField(max_length=50,null=True,blank=True)
#     def __str__(self):
#         return self.name


# class Branch_SKU(models.Model):
#     branch_id = models.ForeignKey(Branch, on_delete=models.CASCADE)
#     sku_id = models.ForeignKey(SKU_SNP, on_delete=models.CASCADE)
#     msl = models.IntegerField(default=None)
#     CreatedDate= models.DateField(auto_now_add=True)
#     CreatedBy=models.ForeignKey(User,on_delete=models.CASCADE)
#     UpdatedDate=models.DateField(auto_now=True)
#     UpdatedBy=models.IntegerField(default=None,blank=True,null=True)
#     Status=models.IntegerField(choices=STATUS_CHOICES)
#     def __str__(self):
#         return self.branch_id

# class Production_Plant(models.Model):
#     Name=models.CharField(max_length=300,null=True,blank=True)
#     location=models.CharField(max_length=200,null=True,blank=True)
#     CreatedDate= models.DateField(auto_now_add=True)
#     CreatedBy=models.ForeignKey(User,on_delete=models.CASCADE)
#     UpdatedDate=models.DateField(auto_now=True)
#     UpdatedBy=models.IntegerField(default=None,blank=True,null=True)
#     Status=models.IntegerField(choices=STATUS_CHOICES)
#     def __str__(self):
#         return self.name

# class Production_Plant_SKU(models.Model):
#     production_plant_id = models.ForeignKey(Production_Plant, on_delete=models.CASCADE)
#     sku_id = models.ForeignKey(SKU_SNP, on_delete=models.CASCADE)
#     CreatedDate= models.DateField(auto_now_add=True)
#     CreatedBy=models.ForeignKey(User,on_delete=models.CASCADE)
#     UpdatedDate=models.DateField(auto_now=True)
#     UpdatedBy=models.IntegerField(default=None,blank=True,null=True)
#     Status=models.IntegerField(choices=STATUS_CHOICES)
#     def __str__(self):
#         return self.name





