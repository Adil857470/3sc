from django.shortcuts import render
from rest_framework.views import APIView
# from rest_framework.response import Response, httpResponse
from django.http import HttpResponse
# from .models import *
import pandas
from . models import ScmUser,Channel,Tenant,BU,Division,Category,Branch,SKU_SNP,Brand,Network
from . models import Branch_SKU,Production_Plant,Production_Plant_SKU

# Create your views here.

class ListUsers(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAdminUser]

    def get(self, *args, **kwargs):
        """
        Return a list of all users.
        """
        tenant_id = Tenant.objects.get(Id=19)
        excel_data_df = pandas.read_excel("C:/Users/adilk/Downloads/upload.xlsx", sheet_name='Production Plant-SKU Mapping')
        get_all_header = excel_data_df.columns.ravel()
        excel_data_df = pandas.read_excel("C:/Users/adilk/Downloads/upload.xlsx", sheet_name='Production Plant-SKU Mapping', usecols=get_all_header)
        excel_to_dict = excel_data_df.to_dict(orient='record')
        ID = 1
        for data in excel_to_dict:
            activity = Production_Plant_SKU()
            if 'Id' in data.keys():
                activity.Id = data['Id']
            else:
                activity.Id = ID
                ID = ID + 1
            # activity.TenantId = tenant_id
            # activity.BUId = BU.objects.filter(Id=data['BUId']).first()
            activity.ProductionPlantId = Production_Plant.objects.filter(Id=data['Production Plant Id']).first()
            # activity.SupplyBranch = Branch.objects.filter(Id=data['Supply Branch Id']).first()
            # activity.BranchId = Branch.objects.filter(Id=data['Branch Id']).first()
            activity.SKUId = SKU_SNP.objects.filter(Id=data['SKU Id']).first()
            # activity.MSL = data['MSL']
            # activity.SupplyBranchType = data['Supply Branch Type']
            # activity.DemandBranch = data['Demand Branch Type']
            # activity.DemandBranchType = data['Demand Branch Type']
            # activity.DeliveryLeadTime = data['Delivery Lead Time']
            # activity.Code = data['Code']
            # activity.Name = data['Name']
            # activity.Location = data['Location']
            # activity.Description = data['Description']
            # activity.UOM = data['UOM']
            # activity.CategoryId = Category.objects.filter(Id=data['CategoryId']).first()
            # activity.DivisionId = Division.objects.filter(Id=data['DivisionID']).first()
            # activity.Brand = Brand.objects.filter(Id=data['Brand']).first()
            # activity.LeadTime = data['LeadTime']

            # activity.channelID = Channel.objects.filter(Id=data['ChannelId']).first()
            activity.CreatedBy = ScmUser.object.filter(email=data['CreatedBy']).first()
            # activity.BranchType = data['Branch Type']
            activity.IPAddress = data['IPAddress']
            activity.Status = data['Status']
            print("channel -------------save")
            activity.save()
        # usernames = [user.username for user in User.objects.all()]
        return HttpResponse({"response":"DONE"})