from django.db import models
from django.contrib.auth.models import User
# Create your models here.
STATUS_CHOICES = (
        ('Active', '1'),
        ('In-Active', '2'),
        )

class Tenant(models.Model):
    code=models.CharField(max_length=200,null=True,blank=True)
    name=models.CharField(max_length=300,null=True,blank=True)
    description=models.TextField()
    created_date= models.DateField(auto_now_add=True)
    created_by=models.OneToOneField(User,on_delete=models.CASCADE)
    updated_date=models.DateField(auto_now=True)
    updated_by=models.IntegerField(default=None,blank=True,null=True)
    ip_address = models.GenericIPAddressField()
    status=models.IntegerField(choices=STATUS_CHOICES)
    def __str__(self):
        return self.name


class Channel(models.Model):
    tenant_id = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    code=models.CharField(max_length=200,null=True,blank=True)
    name=models.CharField(max_length=300,null=True,blank=True)
    description=models.TextField()
    created_date= models.DateField(auto_now_add=True)
    created_by=models.OneToOneField(User,on_delete=models.CASCADE)
    updated_date=models.DateField(auto_now=True)
    updated_by=models.IntegerField(default=None,blank=True,null=True)
    ip_address = models.GenericIPAddressField()
    status=models.IntegerField(choices=STATUS_CHOICES)
    def __str__(self):
        return self.name

class BU(models.Model):
    tenant_id = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    code=models.CharField(max_length=200,null=True,blank=True)
    name=models.CharField(max_length=300,null=True,blank=True)
    description=models.TextField()
    created_date= models.DateField(auto_now_add=True)
    created_by=models.OneToOneField(User,on_delete=models.CASCADE)
    updated_date=models.DateField(auto_now=True)
    updated_by=models.IntegerField(default=None,blank=True,null=True)
    ip_address = models.GenericIPAddressField()
    status=models.IntegerField(choices=STATUS_CHOICES)
    channelid=models.ForeignKey(Channel, on_delete=models.CASCADE)
    def __str__(self):
        return self.name


class Division(models.Model):
    tenant_id = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    code=models.CharField(max_length=200,null=True,blank=True)
    name=models.CharField(max_length=300,null=True,blank=True)
    description=models.TextField()
    created_date= models.DateField(auto_now_add=True)
    created_by=models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    updated_date=models.DateField(auto_now=True)
    updated_by=models.IntegerField(default=None,blank=True,null=True)
    status=models.IntegerField(choices=STATUS_CHOICES)
    ip_address = models.GenericIPAddressField()
    def __str__(self):
        return self.name


class Category(models.Model):
    tenant_id = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    code=models.CharField(max_length=200,null=True,blank=True)
    name=models.CharField(max_length=300,null=True,blank=True)
    description=models.TextField()
    created_date= models.DateField(auto_now_add=True)
    created_by=models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    updated_date=models.DateField(auto_now=True)
    updated_by=models.IntegerField(default=None,blank=True,null=True)
    status=models.IntegerField(choices=STATUS_CHOICES)
    ip_address = models.GenericIPAddressField()
    def __str__(self):
        return self.name

class Brand(models.Model):
    tenant_id = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    code=models.CharField(max_length=200,null=True,blank=True)
    name=models.CharField(max_length=300,null=True,blank=True)
    description=models.TextField()
    created_date= models.DateField(auto_now_add=True)
    created_by=models.OneToOneField(User,on_delete=models.CASCADE)
    updated_date=models.DateField(auto_now=True)
    updated_by=models.IntegerField(default=None,blank=True,null=True)
    status=models.IntegerField(choices=STATUS_CHOICES)
    ip_address = models.GenericIPAddressField()
    def __str__(self):
        return self.name


class tblForecastDtl(models.Model):
    forecastid=models.PositiveIntegerField()
    productid=models.PositiveIntegerField()
    compid=models.PositiveIntegerField()
    salesmonth=models.DateField()
    salesyear=models.DateField()
    salesdate=models.DateField()
    statsqty=models.CharField(max_length=200,null=True,blank=True)
    oprtnqty=models.CharField(max_length=250)
    asp=models.CharField(max_length=250)
    abc=models.CharField(max_length=200,null=True,blank=True)
    mo_qty_3sc=models.CharField(max_length=250)
    m1_qty_3sc=models.CharField(max_length=250)
    def __str__(self):
        return self.forecastid



class SalesOrder_Exim_SFTP(models.Model):
    order_no=models.PositiveIntegerField()
    order_date=models.DateField()
    pick_slip_no=models.PositiveIntegerField()
    shipper_exporter_name=models.CharField(max_length=300,null=True,blank=True)
    shipper_exporter_address=models.CharField(max_length=600,null=True,blank=True)
    consignee_name=models.CharField(max_length=300,null=True,blank=True)
    consignee_address=models.CharField(max_length=600,null=True,blank=True)
    warehouse_code=models.PositiveIntegerField()
    warehouse_name=models.CharField(max_length=400,null=True,blank=True)
    warehouse_address=models.CharField(max_length=600,null=True,blank=True)
    bill_to_name=models.CharField(max_length=300,null=True,blank=True)
    def __str__(self):
        return self.order_no

class Branch(models.Model):
    tenant_id = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    code=models.CharField(max_length=200,null=True,blank=True)
    name=models.CharField(max_length=300,null=True,blank=True)
    description=models.TextField()
    UOM = models.CharField(max_length=100,null=True,blank=True)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    division_id = models.ForeignKey(Division, on_delete=models.CASCADE)
    brand_id = models.ForeignKey(Brand, on_delete=models.CASCADE)
    status=models.IntegerField(choices=STATUS_CHOICES)
    lead_time = models.CharField(max_length=100,null=True,blank=True)
    created_date= models.DateField(auto_now_add=True)
    created_by=models.OneToOneField(User,on_delete=models.CASCADE)
    updated_date=models.DateField(auto_now=True)
    updated_by=models.IntegerField(default=None,blank=True,null=True)
    ip_address = models.GenericIPAddressField()
    def __str__(self):
        return self.name

class SKU_SNP(models.Model):
    tenant_id = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    bu_id = models.ForeignKey(BU, on_delete=models.CASCADE)
    code=models.CharField(max_length=200,null=True,blank=True)
    name=models.CharField(max_length=300,null=True,blank=True)
    description=models.TextField()
    branch_type = models.CharField(max_length=100,null=True,blank=True)
    total_volume = models.CharField(max_length=100,null=True,blank=True)
    total_area = models.CharField(max_length=100,null=True,blank=True)
    operating_hours = models.CharField(max_length=100,null=True,blank=True)
    operting_days = models.CharField(max_length=100,null=True,blank=True)
    operating_times = models.CharField(max_length=100,null=True,blank=True)
    uploading_times = models.CharField(max_length=100,null=True,blank=True)
    created_date= models.DateField(auto_now_add=True)
    created_by=models.OneToOneField(User,on_delete=models.CASCADE)
    updated_date=models.DateField(auto_now=True)
    updated_by=models.IntegerField(default=None,blank=True,null=True)
    status=models.IntegerField(choices=STATUS_CHOICES)
    ip_address = models.GenericIPAddressField()
    def __str__(self):
        return self.name


class Branch_SKU(models.Model):
    branch_id = models.ForeignKey(Branch, on_delete=models.CASCADE)
    sku_id = models.ForeignKey(SKU_SNP, on_delete=models.CASCADE)
    msl = models.IntegerField(default=None)
    created_date= models.DateField(auto_now_add=True)
    created_by=models.OneToOneField(User,on_delete=models.CASCADE)
    updated_date=models.DateField(auto_now=True)
    updated_by=models.IntegerField(default=None,blank=True,null=True)
    status=models.IntegerField(choices=STATUS_CHOICES)
    def __str__(self):
        return self.branch_id

class Production_Plant(models.Model):
    name=models.CharField(max_length=300,null=True,blank=True)
    location=models.CharField(max_length=200,null=True,blank=True)
    created_date= models.DateField(auto_now_add=True)
    created_by=models.OneToOneField(User,on_delete=models.CASCADE)
    updated_date=models.DateField(auto_now=True)
    updated_by=models.IntegerField(default=None,blank=True,null=True)
    status=models.IntegerField(choices=STATUS_CHOICES)
    def __str__(self):
        return self.name

class Production_Plant_SKU(models.Model):
    production_plant_id = models.ForeignKey(Production_Plant, on_delete=models.CASCADE)
    sku_id = models.ForeignKey(SKU_SNP, on_delete=models.CASCADE)
    created_date= models.DateField(auto_now_add=True)
    created_by=models.OneToOneField(User,on_delete=models.CASCADE)
    updated_date=models.DateField(auto_now=True)
    updated_by=models.IntegerField(default=None,blank=True,null=True)
    status=models.IntegerField(choices=STATUS_CHOICES)
    def __str__(self):
        return self.name





