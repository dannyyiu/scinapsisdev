from django.contrib import admin
from search.models import *
# Register your models here.
from templatetags import search_filters


def make_figure_list_hidden(modeladmin, request, queryset):
    queryset.update(is_shown=False)
make_figure_list_hidden.short_description = "Hide selected listings"

def make_figure_list_show(modeladmin, request, queryset):
    queryset.update(is_shown=True)
make_figure_list_show.short_description = "Show selected listings"

@admin.register(PubTechProdResult)
class AdminPubTechProdResult(admin.ModelAdmin):
    raw_id_fields = ('figure', 'doc', 'prod')
    exclude = ('id',)
    list_display = ('figure_thumbnail','figure_header','doc_title', 'sentence','supplier',
        'catalog_nb', 'product_name', 'tech_parental_name', 'technique_group','is_shown')
    #fields = ('doc', 'figure', 'prod', 'supplier', 'catalog_nb', 'product_name', 'tech_parental_name', 'technique_group')

    related_lookup_fields = {
        'fk': ['figure_id', 'doc_id', 'prod_id'],
    }

    search_fields = ['prod__catalog_nb','prod__product_desc','doc__title','figure__header']
    list_filter = ('supplier','technique_group','doc__pub_date')
    change_list_template = "admin/change_list_filter_sidebar.html"
    actions = [make_figure_list_hidden, make_figure_list_show]

    def doc_title(self, obj):
        return obj.doc.title
    def figure_header(self, obj):
        return obj.figure.header
    def figure_url(self, obj):
        return obj.figure.url
    def figure_thumbnail(self, obj):
        url = search_filters.plosone_figure_url(obj.figure.thumbnail,'small')
        return '<img src="%s" />' % url
    figure_thumbnail.allow_tags = True

@admin.register(ScinPubMeta)
class AdminDoc(admin.ModelAdmin):
    from django.contrib.admin import DateFieldListFilter
    exclude=('id',)
    list_display = ('title','author','publisher','pub_date')
    search_fields = ['title','author']
    list_filter = ('publisher',('pub_date',DateFieldListFilter))
    change_list_template = "admin/change_list_filter_sidebar.html"

@admin.register(ScinPubFigure)
class AdminFigure(admin.ModelAdmin):
    raw_id_fields = ('doc',)
    exclude=('id','figure_id')
    list_display = ('figure_thumbnail','header','content','doc')
    search_fields = ['header','content','doc__title']

    def figure_thumbnail(self, obj):
        url = search_filters.plosone_figure_url(obj.thumbnail,'small')
        return '<img src="%s" />' % url
    figure_thumbnail.allow_tags = True

@admin.register(PubProductInfo)
class AdminPubProductInfo(admin.ModelAdmin):
    list_display = ('catalog_nb','product_desc','supplier','url_link')
    exclude = ('id','supplier_0')
    list_filter = ('supplier',)
    search_fields = ['catalog_nb','product_desc']
    change_list_template = "admin/change_list_filter_sidebar.html"

    def url_link(self, obj):
        return '<a href="%s">%s</a>' % (obj.url,obj.url)
    url_link.allow_tags = True

@admin.register(PubProductName)
class AdminPubProductName(admin.ModelAdmin):
    pass


