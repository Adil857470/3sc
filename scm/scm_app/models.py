from django.db import models
from django.contrib.auth.models import User
# Create your models here.
STATUS_CHOICES = (
        (1, 'Active'),
        (0, 'In-Active'),
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

class Channel(models.Model):
    Id = models.IntegerField(primary_key=True)
    TenantId = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    Code=models.CharField(max_length=300,null=True,blank=True)
    Name=models.CharField(max_length=300,null=True,blank=True)
    Description=models.TextField()
    CreatedDate= models.DateField(auto_now_add=True)
    CreatedBy=models.ForeignKey(ScmUser,on_delete=models.CASCADE)
    UpdatedDate=models.DateField(auto_now=True,null=True,blank=True)
    UpdatedBy=models.IntegerField(default=None,blank=True,null=True)
    IPAddress = models.CharField(max_length=300,null=True,blank=True)
    Status=models.IntegerField(choices=STATUS_CHOICES)
#trying for this........
class BU(models.Model):
    Id = models.IntegerField(primary_key=True)
    TenantId = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    Code=models.CharField(max_length=300,null=True,blank=True)
    Name=models.CharField(max_length=300,null=True,blank=True)
    Description=models.TextField()
    CreatedDate= models.DateTimeField(auto_now_add=True)
    CreatedBy=models.ForeignKey(ScmUser,on_delete=models.CASCADE)
    UpdatedDate=models.DateField(auto_now=True,null=True,blank=True)
    UpdatedBy=models.IntegerField(default=None,blank=True,null=True)
    IPAddress = models.CharField(max_length=300,null=True,blank=True)
    Status=models.IntegerField(choices=STATUS_CHOICES)
    channelID=models.ForeignKey(Channel, on_delete=models.CASCADE)

class Division(models.Model):
    Id = models.IntegerField(primary_key=True)
    TenantId = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    Code=models.CharField(max_length=300,null=True,blank=True)
    Name=models.CharField(max_length=300,null=True,blank=True)
    Description=models.TextField()
    CreatedDate= models.DateField(auto_now_add=True)
    CreatedBy=models.ForeignKey(ScmUser,on_delete=models.CASCADE)
    UpdatedDate=models.DateField(auto_now=True,null=True,blank=True)
    UpdatedBy=models.IntegerField(default=None,blank=True,null=True)
    Status=models.IntegerField(choices=STATUS_CHOICES)
    IPAddress = models.CharField(max_length=300,null=True,blank=True)

class Category(models.Model):
    Id = models.IntegerField(primary_key=True)
    TenantId = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    Code=models.CharField(max_length=300,null=True,blank=True)
    Name=models.CharField(max_length=300,null=True,blank=True)
    Description=models.TextField()
    CreatedDate= models.DateField(auto_now_add=True)
    CreatedBy=models.ForeignKey(ScmUser,on_delete=models.CASCADE)
    UpdatedDate=models.DateField(auto_now=True,null=True,blank=True)
    UpdatedBy=models.IntegerField(default=None,blank=True,null=True)
    Status=models.IntegerField(choices=STATUS_CHOICES)
    IPAddress = models.CharField(max_length=300,null=True,blank=True)

class Brand(models.Model):
    Id = models.IntegerField(primary_key=True)
    TenantId = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    Code=models.CharField(max_length=300,null=True,blank=True)
    Name=models.CharField(max_length=300,null=True,blank=True)
    Description=models.TextField()
    CreatedDate= models.DateField(auto_now_add=True)
    CreatedBy=models.ForeignKey(ScmUser,on_delete=models.CASCADE)
    UpdatedDate=models.DateField(auto_now=True,null=True,blank=True)
    UpdatedBy=models.IntegerField(default=None,blank=True,null=True)
    Status=models.IntegerField(choices=STATUS_CHOICES)
    IPAddress = models.CharField(max_length=300,null=True,blank=True)

class Branch(models.Model):
    Id = models.IntegerField(primary_key=True)
    TenantId = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    BUId = models.ForeignKey(BU, on_delete=models.CASCADE)
    channelID=models.ForeignKey(Channel, on_delete=models.CASCADE)
    Code=models.CharField(max_length=300,null=True,blank=True)
    Name=models.CharField(max_length=300,null=True,blank=True)
    Description=models.TextField()
    BranchType = models.CharField(max_length=300,null=True,blank=True)
    TotalVolume = models.CharField(max_length=100,null=True,blank=True)
    TotalArea = models.CharField(max_length=100,null=True,blank=True)
    OperatinHours = models.CharField(max_length=100,null=True,blank=True)
    OpertingDaysoftheWeek = models.CharField(max_length=100,null=True,blank=True)
    operating_times = models.CharField(max_length=100,null=True,blank=True)
    LoadingTimes = models.CharField(max_length=100,null=True,blank=True)
    UnloadingTimes = models.CharField(max_length=100,null=True,blank=True)
    CreatedDate= models.DateField(auto_now_add=True)
    CreatedBy=models.ForeignKey(ScmUser,on_delete=models.CASCADE)
    UpdatedDate=models.DateField(auto_now=True,null=True,blank=True)
    UpdatedBy=models.IntegerField(default=None,blank=True,null=True)
    IPAddress = models.CharField(max_length=300,null=True,blank=True)
    Status=models.IntegerField(choices=STATUS_CHOICES)

class SKU_SNP(models.Model):
    Id = models.IntegerField(primary_key=True)
    TenantId = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    BUId = models.ForeignKey(BU, on_delete=models.CASCADE)
    Code=models.CharField(max_length=300,null=True,blank=True)
    Name=models.CharField(max_length=300,null=True,blank=True)
    Description=models.TextField()
    UOM = models.CharField(max_length=100,null=True,blank=True)
    CategoryId = models.ForeignKey(Category, on_delete=models.CASCADE)
    DivisionId = models.ForeignKey(Division, on_delete=models.CASCADE)
    Brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    LeadTime = models.CharField(max_length=100,null=True,blank=True)
    CreatedDate= models.DateField(auto_now_add=True)
    CreatedBy=models.ForeignKey(ScmUser,on_delete=models.CASCADE)
    UpdatedDate=models.DateField(auto_now=True,null=True,blank=True)
    UpdatedBy=models.IntegerField(default=None,blank=True,null=True)
    Status=models.IntegerField(choices=STATUS_CHOICES)
    IPAddress = models.CharField(max_length=300,null=True,blank=True)

class Network(models.Model):
    Id = models.IntegerField(primary_key=True)
    SupplyBranch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    SupplyBranchType = models.CharField(max_length=300,null=True,blank=True)
    DemandBranch = models.CharField(max_length=300,null=True,blank=True)
    DemandBranchType = models.CharField(max_length=300,null=True,blank=True)
    DeliveryLeadTime = models.CharField(max_length=300,null=True,blank=True)
    CreatedDate= models.DateField(auto_now_add=True)
    CreatedBy=models.ForeignKey(ScmUser,on_delete=models.CASCADE)
    UpdatedDate=models.DateField(auto_now=True,null=True,blank=True)
    UpdatedBy=models.IntegerField(default=None,blank=True,null=True)
    IPAddress = models.CharField(max_length=300,null=True,blank=True)

class Branch_SKU(models.Model):
    Id = models.IntegerField(primary_key=True)
    BranchId = models.ForeignKey(Branch, on_delete=models.CASCADE)
    SkuId = models.ForeignKey(SKU_SNP, on_delete=models.CASCADE)
    MSL = models.IntegerField(default=None)
    CreatedDate= models.DateField(auto_now_add=True)
    CreatedBy=models.ForeignKey(ScmUser,on_delete=models.CASCADE)
    UpdatedDate=models.DateField(auto_now=True,null=True,blank=True)
    UpdatedBy=models.IntegerField(default=None,blank=True,null=True)
    Status=models.IntegerField(choices=STATUS_CHOICES)

class Production_Plant(models.Model):
    Id = models.IntegerField(primary_key=True)
    Name=models.CharField(max_length=300,null=True,blank=True)
    Location=models.CharField(max_length=300,null=True,blank=True)
    CreatedDate= models.DateField(auto_now_add=True)
    CreatedBy=models.ForeignKey(ScmUser,on_delete=models.CASCADE)
    UpdatedDate=models.DateField(auto_now=True,null=True,blank=True)
    UpdatedBy=models.IntegerField(default=None,blank=True,null=True)
    IPAddress = models.CharField(max_length=300,null=True,blank=True)
    Status=models.IntegerField(choices=STATUS_CHOICES)

class Production_Plant_SKU(models.Model):
    Id = models.IntegerField(primary_key=True)
    ProductionPlantId = models.ForeignKey(Production_Plant, on_delete=models.CASCADE)
    SKUId = models.ForeignKey(SKU_SNP, on_delete=models.CASCADE)
    CreatedDate= models.DateField(auto_now_add=True)
    CreatedBy=models.ForeignKey(ScmUser,on_delete=models.CASCADE)
    UpdatedDate=models.DateField(auto_now=True,null=True,blank=True)
    UpdatedBy=models.IntegerField(default=None,blank=True,null=True)
    IPAddress = models.CharField(max_length=300,null=True,blank=True)
    Status=models.IntegerField(choices=STATUS_CHOICES)





