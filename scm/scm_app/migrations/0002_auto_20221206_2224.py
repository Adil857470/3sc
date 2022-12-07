# Generated by Django 3.2.16 on 2022-12-06 16:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0012_alter_user_first_name_max_length'),
        ('scm_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=200, null=True)),
                ('name', models.CharField(blank=True, max_length=300, null=True)),
                ('description', models.TextField()),
                ('UOM', models.CharField(blank=True, max_length=100, null=True)),
                ('status', models.IntegerField(choices=[('Active', '1'), ('In-Active', '2')])),
                ('lead_time', models.CharField(blank=True, max_length=100, null=True)),
                ('created_date', models.DateField(auto_now_add=True)),
                ('updated_date', models.DateField(auto_now=True)),
                ('updated_by', models.IntegerField(blank=True, default=None, null=True)),
                ('ip_address', models.GenericIPAddressField()),
            ],
        ),
        migrations.CreateModel(
            name='BU',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=200, null=True)),
                ('name', models.CharField(blank=True, max_length=300, null=True)),
                ('description', models.TextField()),
                ('created_date', models.DateField(auto_now_add=True)),
                ('updated_date', models.DateField(auto_now=True)),
                ('updated_by', models.IntegerField(blank=True, default=None, null=True)),
                ('ip_address', models.GenericIPAddressField()),
                ('status', models.IntegerField(choices=[('Active', '1'), ('In-Active', '2')])),
            ],
        ),
        migrations.CreateModel(
            name='Production_Plant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=300, null=True)),
                ('location', models.CharField(blank=True, max_length=200, null=True)),
                ('created_date', models.DateField(auto_now_add=True)),
                ('updated_date', models.DateField(auto_now=True)),
                ('updated_by', models.IntegerField(blank=True, default=None, null=True)),
                ('status', models.IntegerField(choices=[('Active', '1'), ('In-Active', '2')])),
                ('created_by', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SalesOrder_Exim_SFTP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_no', models.PositiveIntegerField()),
                ('order_date', models.DateField()),
                ('pick_slip_no', models.PositiveIntegerField()),
                ('shipper_exporter_name', models.CharField(blank=True, max_length=300, null=True)),
                ('shipper_exporter_address', models.CharField(blank=True, max_length=600, null=True)),
                ('consignee_name', models.CharField(blank=True, max_length=300, null=True)),
                ('consignee_address', models.CharField(blank=True, max_length=600, null=True)),
                ('warehouse_code', models.PositiveIntegerField()),
                ('warehouse_name', models.CharField(blank=True, max_length=400, null=True)),
                ('warehouse_address', models.CharField(blank=True, max_length=600, null=True)),
                ('bill_to_name', models.CharField(blank=True, max_length=300, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='tblForecastDtl',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('forecastid', models.PositiveIntegerField()),
                ('productid', models.PositiveIntegerField()),
                ('compid', models.PositiveIntegerField()),
                ('salesmonth', models.DateField()),
                ('salesyear', models.DateField()),
                ('salesdate', models.DateField()),
                ('statsqty', models.CharField(blank=True, max_length=200, null=True)),
                ('oprtnqty', models.CharField(max_length=250)),
                ('asp', models.CharField(max_length=250)),
                ('abc', models.CharField(blank=True, max_length=200, null=True)),
                ('mo_qty_3sc', models.CharField(max_length=250)),
                ('m1_qty_3sc', models.CharField(max_length=250)),
            ],
        ),
        migrations.AlterField(
            model_name='tenant',
            name='code',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='tenant',
            name='created_date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='tenant',
            name='name',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='tenant',
            name='updated_date',
            field=models.DateField(auto_now=True),
        ),
        migrations.CreateModel(
            name='SKU_SNP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=200, null=True)),
                ('name', models.CharField(blank=True, max_length=300, null=True)),
                ('description', models.TextField()),
                ('branch_type', models.CharField(blank=True, max_length=100, null=True)),
                ('total_volume', models.CharField(blank=True, max_length=100, null=True)),
                ('total_area', models.CharField(blank=True, max_length=100, null=True)),
                ('operating_hours', models.CharField(blank=True, max_length=100, null=True)),
                ('operting_days', models.CharField(blank=True, max_length=100, null=True)),
                ('operating_times', models.CharField(blank=True, max_length=100, null=True)),
                ('uploading_times', models.CharField(blank=True, max_length=100, null=True)),
                ('created_date', models.DateField(auto_now_add=True)),
                ('updated_date', models.DateField(auto_now=True)),
                ('updated_by', models.IntegerField(blank=True, default=None, null=True)),
                ('status', models.IntegerField(choices=[('Active', '1'), ('In-Active', '2')])),
                ('ip_address', models.GenericIPAddressField()),
                ('bu_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scm_app.bu')),
                ('created_by', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('tenant_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scm_app.tenant')),
            ],
        ),
        migrations.CreateModel(
            name='Production_Plant_SKU',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateField(auto_now_add=True)),
                ('updated_date', models.DateField(auto_now=True)),
                ('updated_by', models.IntegerField(blank=True, default=None, null=True)),
                ('status', models.IntegerField(choices=[('Active', '1'), ('In-Active', '2')])),
                ('created_by', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('production_plant_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scm_app.production_plant')),
                ('sku_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scm_app.sku_snp')),
            ],
        ),
        migrations.CreateModel(
            name='Division',
            fields=[
                ('code', models.CharField(blank=True, max_length=200, null=True)),
                ('name', models.CharField(blank=True, max_length=300, null=True)),
                ('description', models.TextField()),
                ('created_date', models.DateField(auto_now_add=True)),
                ('created_by', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='auth.user')),
                ('updated_date', models.DateField(auto_now=True)),
                ('updated_by', models.IntegerField(blank=True, default=None, null=True)),
                ('status', models.IntegerField(choices=[('Active', '1'), ('In-Active', '2')])),
                ('ip_address', models.GenericIPAddressField()),
                ('tenant_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scm_app.tenant')),
            ],
        ),
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=200, null=True)),
                ('name', models.CharField(blank=True, max_length=300, null=True)),
                ('description', models.TextField()),
                ('created_date', models.DateField(auto_now_add=True)),
                ('updated_date', models.DateField(auto_now=True)),
                ('updated_by', models.IntegerField(blank=True, default=None, null=True)),
                ('ip_address', models.GenericIPAddressField()),
                ('status', models.IntegerField(choices=[('Active', '1'), ('In-Active', '2')])),
                ('created_by', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('tenant_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scm_app.tenant')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('code', models.CharField(blank=True, max_length=200, null=True)),
                ('name', models.CharField(blank=True, max_length=300, null=True)),
                ('description', models.TextField()),
                ('created_date', models.DateField(auto_now_add=True)),
                ('created_by', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='auth.user')),
                ('updated_date', models.DateField(auto_now=True)),
                ('updated_by', models.IntegerField(blank=True, default=None, null=True)),
                ('status', models.IntegerField(choices=[('Active', '1'), ('In-Active', '2')])),
                ('ip_address', models.GenericIPAddressField()),
                ('tenant_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scm_app.tenant')),
            ],
        ),
        migrations.AddField(
            model_name='bu',
            name='channelid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scm_app.channel'),
        ),
        migrations.AddField(
            model_name='bu',
            name='created_by',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='bu',
            name='tenant_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scm_app.tenant'),
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=200, null=True)),
                ('name', models.CharField(blank=True, max_length=300, null=True)),
                ('description', models.TextField()),
                ('created_date', models.DateField(auto_now_add=True)),
                ('updated_date', models.DateField(auto_now=True)),
                ('updated_by', models.IntegerField(blank=True, default=None, null=True)),
                ('status', models.IntegerField(choices=[('Active', '1'), ('In-Active', '2')])),
                ('ip_address', models.GenericIPAddressField()),
                ('created_by', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('tenant_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scm_app.tenant')),
            ],
        ),
        migrations.CreateModel(
            name='Branch_SKU',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('msl', models.IntegerField(default=None)),
                ('created_date', models.DateField(auto_now_add=True)),
                ('updated_date', models.DateField(auto_now=True)),
                ('updated_by', models.IntegerField(blank=True, default=None, null=True)),
                ('status', models.IntegerField(choices=[('Active', '1'), ('In-Active', '2')])),
                ('branch_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scm_app.branch')),
                ('created_by', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('sku_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scm_app.sku_snp')),
            ],
        ),
        migrations.AddField(
            model_name='branch',
            name='brand_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scm_app.brand'),
        ),
        migrations.AddField(
            model_name='branch',
            name='category_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scm_app.category'),
        ),
        migrations.AddField(
            model_name='branch',
            name='created_by',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='branch',
            name='division_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scm_app.division'),
        ),
        migrations.AddField(
            model_name='branch',
            name='tenant_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scm_app.tenant'),
        ),
    ]
