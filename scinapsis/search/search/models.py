# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models


class PubProductInfo(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    supplier = models.ForeignKey('PubSupplierList', blank=True, null=True)
    supplier_0 = models.CharField(db_column='supplier', max_length=100, blank=True)  # Field renamed because of name conflict.
    catalog_nb = models.CharField(max_length=100, blank=True)
    product_desc = models.CharField(max_length=200, blank=True)
    url = models.CharField(max_length=200, blank=True)
    application = models.CharField(max_length=300, blank=True)
    host = models.CharField(max_length=100, blank=True)
    immunogen = models.CharField(max_length=1500, blank=True)
    reactivity_human = models.BooleanField(default=False,blank=True)
    reactivity_mouse = models.BooleanField(default=False,blank=True)
    size = models.CharField(max_length=10, blank=True)
    price_usd = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    primary_accession = models.CharField(max_length=20, blank=True)
    other_accession = models.CharField(max_length=300, blank=True)
    gene_name = models.CharField(max_length=20, blank=True)
    antigen_region = models.CharField(max_length=20, blank=True)
    antigen_source = models.CharField(max_length=150, blank=True)
    clonality = models.CharField(max_length=10, blank=True)

    def __unicode__(self):
        name = self.catalog_nb
        return u'%s' % name

    class Meta:
        managed = False
        db_table = 'pub_product_info'
        verbose_name = 'Product'


class PubProductName(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    prod = models.ForeignKey(PubProductInfo, blank=True, null=True)
    name = models.CharField(max_length=40, blank=True)

    class Meta:
        managed = False
        db_table = 'pub_product_name'
    def __unicode__(self):
        return u'%s' % self.name

class PubProductResult(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    doc = models.ForeignKey('ScinPubMeta', blank=True, null=True)
    prod = models.ForeignKey(PubProductInfo, blank=True, null=True)
    supplier = models.CharField(max_length=100, blank=True)
    catalog_nb = models.CharField(max_length=100, blank=True)

    class Meta:
        managed = False
        db_table = 'pub_product_result'


class PubSupplierList(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    supplier = models.CharField(max_length=100, blank=True)

    def __unicode__(self):
        return u'%s' % self.supplier

    class Meta:
        managed = False
        db_table = 'pub_supplier_list'


class PubSupplierResult(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    doc = models.ForeignKey('ScinPubMeta', blank=True, null=True)
    supplier_id = models.IntegerField(blank=True, null=True)
    supplier = models.CharField(max_length=100, blank=True)

    class Meta:
        managed = False
        db_table = 'pub_supplier_result'


class PubTechProdResult(models.Model):
    doc = models.ForeignKey('ScinPubMeta', blank=True, null=True)
    figure = models.ForeignKey('ScinPubFigure', blank=True, null=True)
    si_id = models.IntegerField(blank=True, null=True)
    tech = models.ForeignKey('PubTechniqueList', blank=True, null=True)
    tech_parental_name = models.CharField(max_length=100, blank=True)
    tech_alternative = models.CharField(max_length=100, blank=True)
    prod = models.ForeignKey(PubProductInfo, blank=True, null=True)
    supplier = models.CharField(max_length=100, blank=True)
    catalog_nb = models.CharField(max_length=100, blank=True)
    product_name = models.CharField(max_length=40, blank=True)
    sentence = models.TextField(blank=True)
    id = models.IntegerField(primary_key=True)  # AutoField?
    technique_group = models.CharField(max_length=100,blank=True)
    is_shown = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'pub_tech_prod_result'
        verbose_name = 'Search List'
    

class PubTechniqueList(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    parental_name = models.CharField(max_length=100, blank=True)
    alternative = models.CharField(max_length=100, blank=True)
    technique_group = models.CharField(max_length=100, blank=True)

    def __unicode__(self):
        return u'%s' % (self.alternative+' | '+self.parental_name)

    class Meta:
        managed = False
        db_table = 'pub_technique_list'


class PubTechniqueResult(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    doc = models.ForeignKey('ScinPubMeta', blank=True, null=True)
    tech = models.ForeignKey(PubTechniqueList, blank=True, null=True)
    tech_parental_name = models.CharField(max_length=100, blank=True)
    tech_alternative = models.CharField(max_length=100, blank=True)
    technique_group = models.CharField(max_length=100, blank=True)

    class Meta:
        managed = False
        db_table = 'pub_technique_result'


class ScinPubFigure(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    figure_id = models.IntegerField()
    header = models.CharField(max_length=800)
    content = models.TextField()
    url = models.CharField(max_length=100)
    doc = models.ForeignKey('ScinPubMeta', blank=True, null=True)
    thumbnail = models.CharField(max_length=200, blank=True)

    def __unicode__(self):
        return u'%s' % self.header

    class Meta:
        managed = False
        db_table = 'scin_pub_figure'
        verbose_name = 'Figure'


class ScinPubMaterialNMethod(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    section_id = models.IntegerField()
    header = models.CharField(max_length=800)
    content_seq = models.IntegerField()
    content = models.TextField()
    doc = models.ForeignKey('ScinPubMeta', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'scin_pub_material_n_method'


class ScinPubMeta(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    doc_id = models.CharField(max_length=100, blank=True)
    src_address = models.CharField(max_length=200, blank=True)
    pdf_address = models.CharField(max_length=200, blank=True)
    publisher = models.CharField(max_length=100)
    title = models.CharField(max_length=800)
    editors = models.CharField(max_length=200)
    pub_date = models.DateField()
    copyright = models.TextField()
    data_availibility = models.TextField()
    funding = models.TextField()
    competing_interest = models.TextField()
    rec_update_time = models.DateTimeField()
    rec_update_by = models.CharField(max_length=20)
    citation_str = models.CharField(max_length=800, blank=True)
    author = models.CharField(max_length=800, blank=True)
    saves = models.IntegerField(blank=True, null=True)
    shares = models.IntegerField(blank=True, null=True)
    views = models.IntegerField(blank=True, null=True)
    citation = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        return u'%s' % (self.title)

    class Meta:
        managed = False
        db_table = 'scin_pub_meta'
        verbose_name = 'Publication'


class ScinPubResult(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    section_id = models.IntegerField()
    header = models.CharField(max_length=800)
    content_seq = models.IntegerField()
    content = models.TextField()
    doc = models.ForeignKey(ScinPubMeta, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'scin_pub_result'


class ScinPubSupportInfo(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    section_id = models.IntegerField()
    header = models.CharField(max_length=800)
    content = models.TextField()
    url = models.CharField(max_length=100)
    doc = models.ForeignKey(ScinPubMeta, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'scin_pub_support_info'
