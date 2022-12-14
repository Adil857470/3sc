import pandas
from . models import ScmUser,Channel,Tenant,BU,Division,Category,Branch,SKU_SNP,Brand,Network,MSL_report
from . models import Branch_SKU,Production_Plant,Production_Plant_SKU,tblForecastDtl,FC_Details,SalesOrder,Fc_Header
from django.db.models import Sum
import statistics
from datetime import datetime



def mslReport(request):
    try:
        sku_id = request.GET.get('sku_id',None)
        allSKU = SKU_SNP.objects.filter(Id=sku_id).first()
        # FOR NOW DEFAULT VALUES FOR NLT , RP AND STP
        MLT = allSKU.LeadTime  #Manufacturing Lead Time
        # NLT = int(MLT.) + 2
        NLT = int(10) + 2
        RP = 2
        STP = 2
        Forecast_No = Fc_Header.objects.filter(TenantId=allSKU.TenantId,BU_Code=allSKU.BUId)
        Forecast_No_For_print = Forecast_No.values().order_by('-FC_date').first()
        Forecast_No = Forecast_No.order_by('-FC_date').first()

        year = datetime.now().year
        month = datetime.now().month
        ForeCastDemand = FC_Details.objects.filter(SKUId=allSKU,Forecast_No=Forecast_No.Forecast_No,BranchId=Forecast_No.BranchID,ChannelId=Forecast_No.Channel_id,).values(
                'M1_3SC_QTY','M2_3SC_QTY','M3_3SC_QTY','M4_3SC_QTY','M5_3SC_QTY','M6_3SC_QTY','M7_3SC_QTY','M8_3SC_QTY','M9_3SC_QTY','M10_3SC_QTY','M11_3SC_QTY','M12_3SC_QTY').distinct()
        ForeCastDemand = ForeCastDemand.first()
        if ForeCastDemand:
            ForeCastDemandList = list(ForeCastDemand.values())
        else:
            ForeCastDemandList = [0]
        SalesDemand = SalesOrder.objects.filter().values().first()
        # D = sum()
        Demand = sum(ForeCastDemandList)
        PI = NLT * Demand # D is demand & NLT= Net Lead Time
        """
        D= Qty based on historical
        Sales / Forecast Qty

        NLT= MLT(Manufacturing Lead Time) + Transport Lead time b/w WH to CDC + Transport Lead time b/w CDC to branch
        """
        CS = Demand * RP #RP= Replenishment Period
        """
        RP= Dispatching Freq.(days) at CDCs & WH. [ Obtained from 1 year Inbound Data – Source to customer]
        """        
        month = 5
        std_data = [0,0,0,0,0,0]
        if len(ForeCastDemandList) > 1:
            if month > 5:
                std_data = ForeCastDemandList[month-6:month]
            else:
                std_data = ForeCastDemandList[0:month]
                ForeCastDemand = FC_Details.objects.filter(SKUId=allSKU,Forecast_No=Forecast_No.Forecast_No,BranchId=Forecast_No.BranchID,ChannelId=Forecast_No.Channel_id,CreatedDate__year=year-1)
                if ForeCastDemand:
                    ForeCastDemand = ForeCastDemand.values(
                    'M1_3SC_QTY','M2_3SC_QTY','M3_3SC_QTY','M4_3SC_QTY','M5_3SC_QTY','M6_3SC_QTY','M7_3SC_QTY','M8_3SC_QTY','M9_3SC_QTY','M10_3SC_QTY','M11_3SC_QTY','M12_3SC_QTY').distinct().first()
                    ForeCastDemand = ForeCastDemand.values()
                    left_month = 6-month
                    std_data = std_data+list(ForeCastDemand)[12-left_month:12]
                else:
                    std_data = std_data
        STD = statistics.stdev(std_data) # for STANDARD DEVIATION 
        # STD = 10 # HAVE TO MAKE IT DYNAMIC 
        SS = ((Demand**2)*(STP**2) + (RP + NLT)*(STD**2)) # multiplying by 0.5 to find square root of data
        SS = SS ** 0.5
        #FORMULA FOR MSL FINAL FORMULA
        MSL = PI + CS + SS 
        """
        PI is Pipeline inventory
        CS is  Cyclic Stock
        SS is Safety Stock
        """
        # Code for generating MSL report into Database.
        MSL_COUNT = list(MSL_report.objects.all())
        if len(MSL_COUNT) > 0:
            MSL_COUNT = len(MSL_COUNT) + 1
        else:
            MSL_COUNT = 1
        
        msl_report_generation = MSL_report()        
        msl_report_generation.Id = MSL_COUNT
        msl_report_generation.JobId = "dummy01"
        msl_report_generation.TenantId = allSKU.TenantId
        msl_report_generation.BUId = allSKU.BUId
        msl_report_generation.BranchId = Forecast_No.BranchID
        msl_report_generation.SKUId = allSKU
        msl_report_generation.SKU_Code = allSKU.Code
        msl_report_generation.DivisionId = allSKU.DivisionId
        msl_report_generation.CategoryId = allSKU.CategoryId
        msl_report_generation.BrandId = allSKU.Brand
        msl_report_generation.MSL = MSL
        msl_report_generation.PI = PI
        msl_report_generation.CS = CS
        msl_report_generation.SS = SS
        msl_report_generation.Demand = Demand
        msl_report_generation.NLT = NLT
        msl_report_generation.MLT = MLT
        msl_report_generation.RP = RP
        # msl_report_generation.SP = ""
        msl_report_generation.STD = STD
        # msl_report_generation.DailySales = ""
        # msl_report_generation.MonthlySales = ""
        msl_report_generation.CurrentMSL = MSL
        msl_report_generation.FinalMSL = MSL
        msl_report_generation.Year = year
        msl_report_generation.Month = month
        msl_report_generation.Status = 1
        # msl_report_generation.ApprovedBy = ""
        # msl_report_generation.ApprovedDate = ""
        # msl_report_generation.CreatedBy =
        # msl_report_generation.UpdatedDate =
        # msl_report_generation.UpdatedBy =
        # msl_report_generation.IPAddress =
        msl_report_generation.save()
        msl_report = MSL_report.objects.filter(Id=msl_report_generation.Id).values().first()
        return msl_report
    except Exception as e:
        return str(e)

    