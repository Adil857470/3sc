from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
# from .models import *
import pandas
from . models import ScmUser,Channel,Tenant,BU,Division,Category,Branch,SKU_SNP,Brand,Network
from . models import Branch_SKU,Production_Plant,Production_Plant_SKU,tblForecastDtl,FC_Details,SalesOrder_Exim_SFTP,Fc_Header
from django.db.models import Sum
import statistics
from datetime import datetime

# Create your views here.
class getMSL(APIView):
    def get(self, *args, **kwargs):
        sku_id = self.request.GET.get('sku_id',None)
        allSKU = SKU_SNP.objects.filter(Id=sku_id).first()
         
        # FOR NOW DEFAULT VALUES FOR NLT , RP AND STP

        NLT = 2
        RP = 2
        STP = 2
        print("SKU_SNP DATA:  ",SKU_SNP.objects.filter(Id=sku_id).values().first())
        print("\n\n")
        Forecast_No = Fc_Header.objects.filter(TenantId=allSKU.TenantId,BU_Code=allSKU.BUId)
        Forecast_No_For_print = Forecast_No.values().order_by('-FC_date').first()
        Forecast_No = Forecast_No.order_by('-FC_date').first()
        print("FORCAST HEADER DATA: ",Forecast_No_For_print)
        # fc = FC_Details.objects.filter(SKUId=allSKU).first()
        # fc.Forecast_No=Forecast_No.Forecast_No
        # fc.BranchId=Forecast_No.BranchID
        # fc.ChannelId=Channel.objects.filter(Id=Forecast_No.Channel_id).first()
        # fc.save()
        # .update(SKUId=allSKU,Forecast_No=Forecast_No.Forecast_No,BranchId=Forecast_No.BranchID,ChannelId=Forecast_No.Channel_id)
        year = datetime.now().year
        month = datetime.now().month
        SKUBasedDemand = FC_Details.objects.filter(SKUId=allSKU,Forecast_No=Forecast_No.Forecast_No,BranchId=Forecast_No.BranchID,ChannelId=Forecast_No.Channel_id,).values(
                'M1_3SC_QTY','M2_3SC_QTY','M3_3SC_QTY','M4_3SC_QTY','M5_3SC_QTY','M6_3SC_QTY','M7_3SC_QTY','M8_3SC_QTY','M9_3SC_QTY','M10_3SC_QTY','M11_3SC_QTY','M12_3SC_QTY').distinct()
        SKUBasedDemand = SKUBasedDemand.first()
        if SKUBasedDemand:
            SKUBasedDemandList = list(SKUBasedDemand.values())
        else:
            SKUBasedDemandList = [0]
        # SKUBasedDemand = FC_Details.objects.filter(SKUId=allSKU,Forecast_No=Forecast_No.Forecast_No,BranchId=Forecast_No.BranchID,ChannelId=Forecast_No.Channel_id).annotate(
        #     SUM_M1_3SC_QTY = Sum('M1_3SC_QTY'),SUM_M2_3SC_QTY=Sum('M2_3SC_QTY'),SUM_M3_3SC_QTY=Sum('M3_3SC_QTY'),SUM_M4_3SC_QTY = Sum('M4_3SC_QTY'),SUM_M5_3SC_QTY = Sum('M5_3SC_QTY'),SUM_M6_3SC_QTY = Sum('M6_3SC_QTY'),SUM_M7_3SC_QTY = Sum('M7_3SC_QTY'),SUM_M8_3SC_QTY = Sum('M8_3SC_QTY'),SUM_M9_3SC_QTY=Sum('M9_3SC_QTY'),SUM_M10_3SC_QTY = Sum('M10_3SC_QTY'),SUM_M11_3SC_QTY = Sum('M11_3SC_QTY'),SUM_M12_3SC_QTY = Sum('M12_3SC_QTY')).values(
        #         'SUM_M1_3SC_QTY','SUM_M2_3SC_QTY','SUM_M3_3SC_QTY','SUM_M4_3SC_QTY','SUM_M5_3SC_QTY','SUM_M6_3SC_QTY','SUM_M7_3SC_QTY','SUM_M8_3SC_QTY','SUM_M9_3SC_QTY','SUM_M10_3SC_QTY','SUM_M11_3SC_QTY','SUM_M12_3SC_QTY').distinct().first()
        D = sum(SKUBasedDemandList)
        print("DEMAND : ",D)
        PI = NLT * D # D is demand & NLT= Net Lead Time
        """
        D= Qty based on historical
        Sales / Forecast Qty

        NLT= MLT(Manufacturing Lead Time) + Transport Lead time b/w WH to CDC + Transport Lead time b/w CDC to branch
        """
        CS = D * RP #RP= Replenishment Period
        """
        RP= Dispatching Freq.(days) at CDCs & WH. [ Obtained from 1 year Inbound Data – Source to customer]
        """
        
        print(year,month)
        month = 5
        std_data = [0,0,0,0,0,0]
        if len(SKUBasedDemandList) > 1:
            if month > 5:
                std_data = SKUBasedDemandList[month-6:month]
            else:
                std_data = SKUBasedDemandList[0:month]
                SKUBasedDemand = FC_Details.objects.filter(SKUId=allSKU,Forecast_No=Forecast_No.Forecast_No,BranchId=Forecast_No.BranchID,ChannelId=Forecast_No.Channel_id,CreatedDate__year=year-1)
                if SKUBasedDemand:
                    SKUBasedDemand = SKUBasedDemand.values(
                    'M1_3SC_QTY','M2_3SC_QTY','M3_3SC_QTY','M4_3SC_QTY','M5_3SC_QTY','M6_3SC_QTY','M7_3SC_QTY','M8_3SC_QTY','M9_3SC_QTY','M10_3SC_QTY','M11_3SC_QTY','M12_3SC_QTY').distinct().first()
                    SKUBasedDemand = SKUBasedDemand.values()
                    left_month = 6-month
                    std_data = std_data+list(SKUBasedDemand)[12-left_month:12]
                else:
                    std_data = std_data
            
        print("std_data : ",std_data)
        STD = statistics.stdev(std_data) # for STANDARD DEVIATION 
        # STD = 10 # HAVE TO MAKE IT DYNAMIC 
        SS = ((D**2)*(STP**2) + (RP + NLT)*(STD**2)) # multiplying by 0.5 to find square root of data
        print("=======SS=======",SS)
        SS = SS ** 0.5
        print("=======SS=======",SS)
        #FORMULA FOR MSL FINAL FORMULA
        MSL = PI + CS + SS 
        """
        PI is Pipeline inventory
        CS is  Cyclic Stock
        SS is Safety Stock
        """
        
        return Response({"MSL":MSL})


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
        excel_data_df = pandas.read_excel("C:/Users/adilk/Downloads/fcHeader.xlsx", sheet_name='Sheet1')
        get_all_header = excel_data_df.columns.ravel()
        excel_data_df = pandas.read_excel("C:/Users/adilk/Downloads/fcHeader.xlsx", sheet_name='Sheet1', usecols=get_all_header)
        excel_to_dict = excel_data_df.to_dict(orient='record')
        ID = 1
        print("DELETING ..........")
        print(BU.objects.all().values().first())
        Fc_Header.objects.all( ).delete()
        # return HttpResponse("DELETED!")
        print("DELETING ..........")
        for data in excel_to_dict:
            activity = Fc_Header()
            # if 'Id' in data.keys():
                # activity.Id = data['Id']
                # activity.forecastid = data['Id']
            # else:
                # activity.Id = ID
                # activity.forecastid = ID
                # ID = ID + 1
            # activity.TenantId = tenant_id
            activity.Id = data[str('ID')]
            tenant_id = Tenant.objects.get(Id=data[str('TenantId')])
            activity.TenantId = tenant_id
            activity.Forecast_No = data[str('Forecast_No')]
            activity.Company_Code = data[str('Company_Code')]
            # activity.shipper_exporter_address = data[str('shipper_exporter_address')]
            activity.FC_Month = data[str('FC_Month')]
            activity.FC_Year = data[str('FC_Year')]
            activity.FC_Generate_dt = data[str('FC_Generate_dt')]
            activity.ASM_Code = data[str('ASM_Code')]
            activity.Territory = data[str('Territory')]
            activity.BranchID = Branch.objects.filter(Id=data[str('BranchID')]).first() 
            activity.BranchDesc = data[str('BranchDesc')]
            activity.State_Code = data[str('State_Code')]
            activity.State_Desc = data[str('State_Desc')]
            activity.Zone = data[str('Zone')]
            print("=====Channel===========",data[str('Channel')])
            activity.Channel = Channel.objects.filter(Id=data['Channel']).first()
            # activity.cust_po_date = data[str('cust_po_date')]
            # activity.gst_invoice_no = data[str('gst_invoice_no')]
            # activity.gst_inv_date = data[str('gst_inv_date')]
            activity.Channel_Desc = data[str('Channel_Desc')]
            activity.BU_Code = BU.objects.filter(Code=data[str('BU_Code')]).first()
            activity.Is_FC_Active = data[str('Is_FC_Active')]
            activity.Is_ASM_Save = data[str('Is_ASM_Save')]
            activity.Is_ASM_Approve = data[str('Is_ASM_Approve')]
            activity.FC_Status = data[str('FC_Status')]
            activity.FC_date = data[str('FC_date')]
            activity.FC_Upload_on = data[str('FC_Upload_on')]
            activity.FC_Upload_ip = data[str('FC_Upload_ip')]
            activity.FC_Approved_by = data[str('FC_Approved_by')]
            activity.FC_Approved_on = data[str('FC_Approved_on')]
            activity.FC_Approved_ip = data[str('FC_Approved_ip')]
            activity.FC_Last_Updated_by = data[str('FC_Last_Updated_by')]
            activity.FC_Last_Updated_on = data[str('FC_Last_Updated_on')]
            # activity.bank_account_no = data[str('bank_account_no')]
            activity.FC_Last_Updated_ip  = data[str('FC_Last_Updated_ip')]
            activity.FC_PendingLevel = data[str('FC_PendingLevel')]
            # activity.swift_code = data[str('swift_code')]
            activity.FC_PendingAt_Role = data[str('FC_PendingAt_Role')]
            activity.FC_PendingAt = data[str('FC_PendingAt')]
            activity.FC_Upload_by = data[str('FC_Upload_by')]
            # activity.shipment_mode = data[str('shipment_mode').upper()]
            # activity.port_of_loading = data[str('port_of_loading').upper()]
            # activity.port_of_discharge = data[str('port_of_discharge').upper()]
            # activity.country_of_origin = data[str('country_of_origin').upper()]
            # activity.state_of_origin = data[str('state_of_origin').upper()]
            # activity.district_of_origin = data[str('district_of_origin').upper()]
            # activity.final_destination = data[str('final_destination').upper()]
            # activity.country_of_final_destination = data[str('country_of_final_destination').upper()]
            # activity.pre_carriage_by = data[str('pre_carriage_by').upper()]
            # activity.place_of_receipt_of_pre_carr = data[str('place_of_receipt_of_pre_carr').upper()]
            # # activity.vessel_flight_no = data[str('vessel_flight_no').upper()]
            # activity.adcode = data[str('adcode').upper()]
            # activity.totalquantity = data[str('totalquantity').upper()]
            # activity.totalnetweight = data[str('totalnetweight').upper()]
            # activity.totalgrossweight = data[str('totalgrossweight').upper()]
            # activity.custom_division = data[str('customs_division').upper()]
            # activity.gstin = data[str('gstin').upper()]
            # activity.name_of_commissionarate = data[str('name_of_commissionarate').upper()]
            # activity.item_code = SKU_SNP.objects.filter(Id=data[str('item_code').upper()]).first()
            # activity.item_description = data[str('item_description').upper()]
            # activity.product_category = data[str('product_category').upper()]
            # activity.hsn_code = data[str('hsn_code').upper()]
            # activity.qty = data[str('qty').upper()]
            # activity.product_category = data[str('product_category').upper()]
            # activity.uom = data[str('uom').upper()]
            # activity.unit_rate = data[str('unit_rate').upper()]
            # # activity.net_weight = data[str('net_weight').upper()]
            # activity.gross_weight = data[str('gross_weight').upper()]
            # activity.total_price = data[str('total_price').upper()]
            # activity.warehousecode = data[str('warehousecode').upper()]
            # activity.header_id = data[str('header_id').upper()]
            # activity.line_id = data[str('line_id').upper()]
            # activity.delivery_detail_id = data[str('delivery_detail_id').upper()]
            # activity.delivery_assignment_id = data[str('delivery_assignment_id').upper()]
            # # activity.delivery_id = data[str('delivery_id').upper()]
            # activity.exim_state_origin = data[str('exim_state_origin').upper()]
            # activity.exim_district_origin = data[str('exim_district_origin').upper()]
            # activity.consignee_country = data[str('consignee_country').upper()]
            # # activity.consignee_tel_no = data[str('consignee_tel_no').upper()]
            # activity.ship_to_details = data[str('ship_to_details').upper()]
            # activity.export_pincode = data[str('export_pincode').upper()]
            # # activity.export_country = data[str('export_country').upper()]
            # # activity.buyer_ord_count_date = data[str('BUYER_ORD_CONT_DATE').upper()]
            # # activity.other_ref_count_tel_no = data[str('OTHER_REF_CONT_TEL_NO').upper()]
            # activity.add_inf_payment_term = data[str('add_inf_payment_term').upper()]
            # activity.hdr_status = data[str('hdr_status').upper()]
            # activity.line_status = data[str('line_status').upper()]
            # activity.shipping_status = data[str('shipping_status').upper()]
            # activity.order_type = data[str('order_type').upper()]
            # activity.reference_type = data[str('Reference_type')]
            # activity.reference_no = data['reference_no']
            # activity.reference_line_no = data['reference_line_no']
            # activity.custom_exchange_currency = data['custom_exchange_currency']
            # activity.custom_exchange_rate = data['custom_exchange_rate']
            # activity.Forecast_No = data['Forecast_No']
            # # print(Channel.objects.filter(Id=data['ChannelId']).first())
            # activity.ChannelId = Channel.objects.filter(Id=data['ChannelId']).first()
            # activity.Channel = data['Channel']
            # activity.BUId = BU.objects.filter(Id=data['BUId']).first()
            # activity.BU = data['BU']
            # activity.DivisionId = Division.objects.filter(Id=data['DivisionId']).first()
            # activity.Division = data['Division']
            # activity.CategoryId = Category.objects.filter(Id=data['CategoryId']).first()
            # activity.Category = data['Category']
            # print(Brand.objects.filter(Id=data['BrandId']).first(),'RAND')
            # activity.BrandId = Brand.objects.filter(Id=data['BrandId']).first()
            # activity.Brand = data['Brand']
            # activity.SKUId = SKU_SNP.objects.filter(Id=data['SKUId']).first()
            # activity.SKU_Code = data['SKU_Code']
            # activity.SKU = data['SKU']
            # activity.SKU_Class = data['SKU_Class']
            # activity.SKU_Status = data['SKU_Status']
            # activity.Region = data['Region']
            # activity.AGGREGATE_SPEC1 = data['AGGREGATE_SPEC1']
            # activity.AGGREGATE_SPEC2 = data['AGGREGATE_SPEC2']
            # activity.DepoCode = data['DepoCode']
            # activity.ASM = data['ASM']
            # activity.LCID = data['LCID']
            # activity.Launch_PLSIND_State = data['Launch_PLSIND_State']
            # activity.Launch_PLSIND_StateFlag = data['Launch_PLSIND_StateFlag']
            # activity.ASP = data['ASP']
            # activity.YTDAvg_Sales = data['YTDAvg_Sales']
            # activity.YTDAvg_Sales_Val = data['YTDAvg_Sales_Val']
            # activity.Twelve_Mon_Avg_Sales = data['Twelve_Mon_Avg_Sales']
            # activity.Twelve_Mon_Avg_Sales_val = data['Twelve_Mon_Avg_Sales_val']
            # activity.Six_Mon_Avg_Sales = data['Six_Mon_Avg_Sales']
            # activity.Six_Mon_Avg_Sales_Val = data['Six_Mon_Avg_Sales_Val']
            # activity.Three_Mon_Avg_Sales = data['Three_Mon_Avg_Sales']
            # activity.Three_Mon_Avg_Sales = data['Three_Mon_Avg_Sales']
            # activity.LM_Sales = data['LM_Sales']
            # activity.LM_Sales_Val = data['LM_Sales_Val']
            # activity.LMFC_Sales = data['LMFC_Sales']
            # activity.LMFC_Sales_Val = data['LMFC_Sales_Val']
            # activity.LYSM1_Sales = data['LYSM1_Sales']
            # activity.LYSM2_Sales = data['LYSM2_Sales']
            # activity.LYSM3_Sales = data['LYSM3_Sales']
            # activity.LYSM4_Sales = data['LYSM4_Sales']
            # activity.LYSM5_Sales = data['LYSM5_Sales']
            # activity.LYSM6_Sales = data['LYSM6_Sales']
            # activity.LYSM1_Sales_Val = data['LYSM1_Sales_Val']
            # activity.LYSM2_Sales_Val = data['LYSM2_Sales_Val']
            # activity.LYSM3_Sales_Val = data['LYSM3_Sales_Val']
            # activity.LYSM4_Sales_Val = data['LYSM4_Sales_Val']
            # activity.LYSM5_Sales_Val = data['LYSM5_Sales_Val']
            # activity.LYSM6_Sales_Val = data['LYSM6_Sales_Val']

            # activity.YTM_AOP = data['YTM_AOP']
            # activity.YTM_AOP_Val = data['YTM_AOP_Val']
            # activity.YTM_Sales = data['YTM_Sales']
            # activity.YTM_Sales_Val = data['YTM_Sales_Val']
            # activity.LTSF_Sales = data['LTSF_Sales']
            # activity.LTSF_Sales_Val = data['LTSF_Sales_Val']
            # activity.LYAS_Sales = data['LYAS_Sales']
            # activity.LYAS_Sales_Val = data['LYAS_Sales_Val']
            # activity.M1_3SC_QTY = data['M1_3SC_QTY']

            # activity.M2_3SC_QTY = data['M2_3SC_QTY']
            # activity.M3_3SC_QTY = data['M3_3SC_QTY']
            # activity.M4_3SC_QTY = data['M4_3SC_QTY']
            # activity.M5_3SC_QTY = data['M5_3SC_QTY']
            # activity.M6_3SC_QTY = data['M6_3SC_QTY']
            # activity.M7_3SC_QTY = data['M7_3SC_QTY']
            # activity.M8_3SC_QTY = data['M8_3SC_QTY']
            # activity.M9_3SC_QTY = data['M9_3SC_QTY']
            # activity.M10_3SC_QTY = data['M10_3SC_QTY']
            # activity.M11_3SC_QTY = data['M11_3SC_QTY']
            # activity.M12_3SC_QTY = data['M12_3SC_QTY']
            # activity.M1_3SC_Val = data['M1_3SC_Val']
            # activity.M2_3SC_Val = data['M2_3SC_Val']
            # activity.M3_3SC_Val = data['M3_3SC_Val']
            # activity.M4_3SC_Val = data['M4_3SC_Val']
            # activity.M5_3SC_Val = data['M5_3SC_Val']
            # activity.M6_3SC_Val = data['M6_3SC_Val']
            # activity.M7_3SC_Val = data['M7_3SC_Val']
            # activity.M8_3SC_Val = data['M8_3SC_Val']
            # activity.M9_3SC_Val = data['M9_3SC_Val']
            # activity.M10_3SC_Val = data['M10_3SC_Val']
            # activity.M11_3SC_Val = data['M11_3SC_Val']
            # activity.M12_3SC_Val = data['M12_3SC_Val']
            
            # activity.M1_OPS_QTY = data['M1_OPS_QTY']
            # activity.M2_OPS_QTY = data['M2_OPS_QTY']
            # activity.M3_OPS_QTY = data['M3_OPS_QTY']
            # activity.M4_OPS_QTY = data['M4_OPS_QTY']
            # activity.M5_OPS_QTY = data['M5_OPS_QTY']
            # activity.M6_OPS_QTY = data['M6_OPS_QTY']
            # activity.M7_OPS_QTY = data['M7_OPS_QTY']
            # activity.M8_OPS_QTY = data['M8_OPS_QTY']
            # activity.M9_OPS_QTY = data['M9_OPS_QTY']
            # activity.M10_OPS_QTY = data['M10_OPS_QTY']
            # activity.M11_OPS_QTY = data['M11_OPS_QTY']
            # activity.M12_OPS_QTY = data['M12_OPS_QTY']
            # activity.M1_OPS_VAL = data['M1_OPS_VAL']
            # activity.M2_OPS_VAL = data['M2_OPS_VAL']
            # activity.M3_OPS_VAL = data['M3_OPS_VAL']
            # activity.M4_OPS_VAL = data['M4_OPS_VAL']
            # activity.M5_OPS_VAL = data['M5_OPS_VAL']
            # activity.M6_OPS_VAL = data['M6_OPS_VAL']
            # activity.M7_OPS_VAL = data['M7_OPS_VAL']
            # activity.M8_OPS_VAL = data['M8_OPS_VAL']
            # activity.M9_OPS_VAL = data['M9_OPS_VAL']
            # activity.M10_OPS_VAL = data['M10_OPS_VAL']
            # activity.M11_OPS_VAL = data['M11_OPS_VAL']
            # activity.M12_OPS_VAL = data['M12_OPS_VAL']

            # activity.M1_SALES_QTY = data['M1_SALES_QTY']
            # activity.M2_SALES_QTY = data['M2_SALES_QTY']
            # activity.M3_SALES_QTY = data['M3_SALES_QTY']
            # activity.M4_SALES_QTY = data['M4_SALES_QTY']
            # activity.M5_SALES_QTY = data['M5_SALES_QTY']
            # activity.M6_SALES_QTY = data['M6_SALES_QTY']
            # activity.M7_SALES_QTY = data['M7_SALES_QTY']
            # activity.M8_SALES_QTY = data['M8_SALES_QTY']
            # activity.M9_SALES_QTY = data['M9_SALES_QTY']
            # activity.M10_SALES_QTY = data['M10_SALES_QTY']
            # activity.M11_SALES_QTY = data['M11_SALES_QTY']
            # activity.M12_SALES_QTY = data['M12_SALES_QTY']
            # activity.M1_SALES_VAL = data['M1_SALES_VAL']
            # activity.M2_SALES_VAL = data['M2_SALES_VAL']
            # activity.M3_SALES_VAL = data['M3_SALES_VAL']
            # activity.M4_SALES_VAL = data['M4_SALES_VAL']
            # activity.M5_SALES_VAL = data['M5_SALES_VAL']
            # activity.M6_SALES_VAL = data['M6_SALES_VAL']
            # activity.M7_SALES_VAL = data['M7_SALES_VAL']
            # activity.M8_SALES_VAL = data['M8_SALES_VAL']
            # activity.M9_SALES_VAL = data['M9_SALES_VAL']
            # activity.M10_SALES_VAL = data['M10_SALES_VAL']
            # activity.M11_SALES_VAL = data['M11_SALES_VAL']
            # activity.M12_SALES_VAL = data['M12_SALES_VAL']

            # activity.M1_AOP_QTY = data['M1_AOP_QTY']
            # activity.M2_AOP_QTY = data['M2_AOP_QTY']
            # activity.M3_AOP_QTY = data['M3_AOP_QTY']
            # activity.M1_AOP_VAL = data['M1_AOP_VAL']
            # activity.M2_AOP_VAL = data['M2_AOP_VAL']
            # activity.M3_AOP_VAL = data['M3_AOP_VAL']
            
            # activity.M1_RTF_QTY = data['M1_RTF_QTY']
            # activity.M2_RTF_QTY = data['M2_RTF_QTY']
            # activity.M3_RTF_QTY = data['M3_RTF_QTY']
            # activity.M1_RTF_VAL = data['M1_RTF_VAL']
            # activity.M2_RTF_VAL = data['M2_RTF_VAL']
            # activity.M3_RTF_VAL = data['M3_RTF_VAL']

            # activity.M1_FINALFC_QTY = data['M1_FINALFC_QTY']
            # activity.M2_FINALFC_QTY = data['M2_FINALFC_QTY']
            # activity.M3_FINALFC_QTY = data['M3_FINALFC_QTY']
            # activity.M1_FINALFC_VAL = data['M1_FINALFC_VAL']
            # activity.M2_FINALFC_VAL = data['M2_FINALFC_VAL']
            # activity.M3_FINALFC_VAL = data['M3_FINALFC_VAL']

            # activity.L12_Min = data['L12_Min']
            # activity.L12_Max = data['L12_Max']
            # activity.L12_Min_VAL = data['L12_Min_VAL']
            # activity.L12_Max_VAL = data['L12_Max_VAL']
            # activity.M_1 = data['M-1']
            # activity.M_2 = data['M-2']
            # activity.M_3 = data['M-3']

            
            # activity.Status = data['Status']
            # activity.Six_Mon_Avg_Forecast = data['Six_Mon_Avg_Forecast']
            # activity.StockTill = data['StockTill']
            # activity.RemarkID = data['RemarkID']
            # activity.Remark = data['Remark']
            # activity.Active = data['Active']
            # activity.Week1_ActualSales = data['Week1_ActualSales']
            # activity.Week2_ActualSales = data['Week2_ActualSales']
            # activity.Week3_ActualSales = data['Week3_ActualSales']
            # activity.Week4_ActualSales = data['Week4_ActualSales']
            # activity.First_Year = data['First_Year']
            # activity.FY_M1_QTY = data['FY_M1_QTY']
            # activity.FY_M2_QTY = data['FY_M2_QTY']
            # activity.FY_M3_QTY = data['FY_M3_QTY']
            # activity.FY_M4_QTY = data['FY_M4_QTY']
            # activity.FY_M5_QTY = data['FY_M5_QTY']
            # activity.FY_M6_QTY = data['FY_M6_QTY']
            # activity.FY_M7_QTY = data['FY_M7_QTY']
            # activity.FY_M8_QTY = data['FY_M8_QTY']
            # activity.FY_M9_QTY = data['FY_M9_QTY']
            # activity.FY_M10_QTY = data['FY_M10_QTY']
            # activity.FY_M11_QTY = data['FY_M11_QTY']
            # activity.FY_M12_QTY = data['FY_M12_QTY']
            # activity.FY_M1_Val = data['FY_M1_VAL']
            # activity.FY_M2_Val = data['FY_M2_VAL']
            # activity.FY_M3_Val = data['FY_M3_VAL']
            # activity.FY_M4_Val = data['FY_M4_VAL']
            # activity.FY_M5_Val = data['FY_M5_VAL']
            # activity.FY_M6_Val = data['FY_M6_VAL']
            # activity.FY_M7_Val = data['FY_M7_VAL']
            # activity.FY_M8_Val = data['FY_M8_VAL']
            # activity.FY_M9_Val = data['FY_M9_VAL']
            # activity.FY_M10_Val = data['FY_M10_VAL']
            # activity.FY_M11_Val = data['FY_M11_VAL']
            # activity.FY_M12_Val = data['FY_M12_VAL']

            # activity.Second_YEAR = data['Second_YEAR']
            # activity.SY_M1_QTY = data['SY_M1_QTY']
            # activity.SY_M2_QTY = data['SY_M2_QTY']
            # activity.SY_M3_QTY = data['SY_M3_QTY']
            # activity.SY_M4_QTY = data['SY_M4_QTY']
            # activity.SY_M5_QTY = data['SY_M5_QTY']
            # activity.SY_M6_QTY = data['SY_M6_QTY']
            # activity.SY_M7_QTY = data['SY_M7_QTY']
            # activity.SY_M8_QTY = data['SY_M8_QTY']
            # activity.SY_M9_QTY = data['SY_M9_QTY']
            # activity.SY_M10_QTY = data['SY_M10_QTY']
            # activity.SY_M11_QTY = data['SY_M11_QTY']
            # activity.SY_M12_QTY = data['SY_M12_QTY']
            # activity.SY_M1_Val = data['SY_M1_VAL']
            # activity.SY_M2_Val = data['SY_M2_VAL']
            # activity.SY_M3_Val = data['SY_M3_VAL']
            # activity.SY_M4_Val = data['SY_M4_VAL']
            # activity.SY_M5_Val = data['SY_M5_VAL']
            # activity.SY_M6_Val = data['SY_M6_VAL']
            # activity.SY_M7_Val = data['SY_M7_VAL']
            # activity.SY_M8_Val = data['SY_M8_VAL']
            # activity.SY_M9_Val = data['SY_M9_VAL']
            # activity.SY_M10_Val = data['SY_M10_VAL']
            # activity.SY_M11_Val = data['SY_M11_VAL']
            # activity.SY_M12_Val = data['SY_M12_VAL']

            # activity.Third_YEAR = data['Third_YEAR']
            # activity.TY_M1_QTY = data['TY_M1_QTY']
            # activity.TY_M2_QTY = data['TY_M2_QTY']
            # activity.TY_M3_QTY = data['TY_M3_QTY']
            # activity.TY_M4_QTY = data['TY_M4_QTY']
            # activity.TY_M5_QTY = data['TY_M5_QTY']
            # activity.TY_M6_QTY = data['TY_M6_QTY']
            # activity.TY_M7_QTY = data['TY_M7_QTY']
            # activity.TY_M8_QTY = data['TY_M8_QTY']
            # activity.TY_M9_QTY = data['TY_M9_QTY']
            # activity.TY_M10_QTY = data['TY_M10_QTY']
            # activity.TY_M11_QTY = data['TY_M11_QTY']
            # activity.TY_M12_QTY = data['TY_M12_QTY']
            # activity.TY_M1_Val = data['TY_M1_VAL']
            # activity.TY_M2_Val = data['TY_M2_VAL']
            # activity.TY_M3_Val = data['TY_M3_VAL']
            # activity.TY_M4_Val = data['TY_M4_VAL']
            # activity.TY_M5_Val = data['TY_M5_VAL']
            # activity.TY_M6_Val = data['TY_M6_VAL']
            # activity.TY_M7_Val = data['TY_M7_VAL']
            # activity.TY_M8_Val = data['TY_M8_VAL']
            # activity.TY_M9_Val = data['TY_M9_VAL']
            # activity.TY_M10_Val = data['TY_M10_VAL']
            # activity.TY_M11_Val = data['TY_M11_VAL']
            # activity.TY_M12_Val = data['TY_M12_VAL']
            
            
            # activity.ProductionPlantId = Production_Plant.objects.filter(Id=data['Production Plant Id']).first()
            # activity.SupplyBranch = Branch.objects.filter(Id=data['Supply Branch Id']).first()
            # activity.BranchId = Branch.objects.filter(Id=data['Branch Id']).first()
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
            # activity.LeadTime = data['LeadTime']
            #### for forcast data 
            # activity.productid = data['ProductID']
            # activity.Compid = data['CompID']
            # activity.salesmonth = data['SalesMnth']
            # activity.salesYr = data['SalesYr']
            # activity.salesDt = data['SalesDt']
            # activity.statsQty = data['StatsQty']
            # activity.OprtnQty = data['OprtnQty']
            # activity.asp = data['ASP']
            # activity.abc = data['ABC']
            # activity.M0_QTY_3SC = data['M0_QTY_3SC']
            # activity.M1_QTY_3SC = data['M1_QTY_3SC']
            # activity.M2_QTY_3SC = data['M2_QTY_3SC']
            # activity.M3_QTY_3SC = data['M3_QTY_3SC']
            # activity.M4_QTY_3SC = data['M4_QTY_3SC']
            # activity.M5_QTY_3SC = data['M5_QTY_3SC']
            # activity.M6_QTY_3SC = data['M6_QTY_3SC']
            # activity.M7_QTY_3SC = data['M7_QTY_3SC']
            # activity.M8_QTY_3SC = data['M8_QTY_3SC']
            # activity.M8_QTY_3SC = data['M8_QTY_3SC']
            # activity.M9_QTY_3SC = data['M9_QTY_3SC']
            # activity.M10_QTY_3SC = data['M10_QTY_3SC']
            # activity.M11_QTY_3SC = data['M11_QTY_3SC']
            # activity.M12_QTY_3SC = data['M12_QTY_3SC']
            # activity.M0_QTY_3SC = data['M0_QTY_3SC']
            # activity.M1_QTY = data['M1_QTY']
            # activity.M2_QTY = data['M2_QTY']
            # activity.M3_QTY = data['M3_QTY']
            # activity.M4_QTY = data['M4_QTY']
            # activity.M5_QTY = data['M5_QTY']
            # activity.M6_QTY = data['M6_QTY']
            # activity.M7_QTY = data['M7_QTY']
            # activity.M8_QTY = data['M8_QTY']
            # activity.M9_QTY = data['M9_QTY']
            # activity.M10_QTY = data['M10_QTY']
            # activity.M11_QTY = data['M11_QTY']
            # activity.M12_QTY = data['M12_QTY']
            # activity.M6_Avg_Sales = data['M6_Avg_Sales']
            # activity.M3_Avg_Sales = data['M3_Avg_Sales']
            # activity.L3M_Qty_Avg = data['L3M_QTY_Avg']
            # activity.LYSM1_Sales = data['LYSM1_Sales']
            # activity.LYSM2_Sales = data['LYSM2_Sales']
            # activity.LYSM3_Sales = data['LYSM3_Sales']
            # activity.LM_Sales = data['LM_Sales']
            # activity.L3M_Pri_QTY = data['L3M_Pri_QTY']
            # activity.ReasonId = data['ReasonId']
            # activity.IsChanged = data['IsChanged']
            # activity.IsApproved = data['IsApproved']
            # activity.SKUStatus = data['SKUStatus']
            # activity.L12Min = data['L12Min']
            # activity.L12Max = data['L12Max']
            # activity.M1 = data['M1']
            # activity.M2 = data['M2']
            # activity.M3 = data['M3']
            # activity.M4 = data['M4']
            # activity.M5 = data['M5']
            # activity.M6 = data['M6']
            # activity.Category = data['Category']
            # activity.Category1 = data['Category1']
            # activity.Line1 = data['Line1']
            # activity.Line2 = data['Line2']
            # activity.Line3 = data['Line3']
            # activity.Line4 = data['Line4']
            # activity.SKU = SKU_SNP.objects.filter(Id=data['SKU']).first()
            # activity.Channel = Channel.objects.filter(Code=data['CHANNEL']).first()
            # activity.LocationID = data['LocationID']

            # activity.channelID = Channel.objects.filter(Id=data['ChannelId']).first()
            # activity.CreatedBy = ScmUser.object.all().first()
            # activity.UpdatedBy = activity.CreatedBy
            # activity.BranchType = data['Branch Type']
            # activity.IPAddress = data['IPAddress']
            print("channel -------------save")
            activity.save()
            # try:
            # except Exception as e:
            #     print("ERROR: \t")
        # usernames = [user.username for user in User.objects.all()]
        return HttpResponse({"response":"DONE"})