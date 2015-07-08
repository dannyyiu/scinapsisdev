from django.shortcuts import render
from search.models import PubTechProdResult, PubProductInfo, ScinPubFigure,PubProductName
from django.db.models import Count
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core import serializers
from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
import logging
from django.template import loader,Context



@csrf_exempt
def typeahead_view(request):
    if request.is_ajax():        
        query = request.GET.get('query',None)  
        if query:    
          product = PubProductName.objects.filter(Q(name__icontains=query)).values('name','id') 
          print product   
          return  JsonResponse(list(product),safe=False)
        else:
            "Prefetch data if no query is provided to increase speed"
            product = PubProductName.objects.all().values('name','id')
            return JsonResponse(list(product),safe=False)

def _get_user_info(req):
    if req.user:
        return req.user
    else:
        return None

def _get_catids_from_q(query):
    if not query:
        return None
   

    cat_ids = PubProductName.objects.filter(Q(name__icontains=query)).values('prod_id').annotate()
    cat_ids = [ i['prod_id'] for i in cat_ids]
    return cat_ids

def logout_view(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect('login')

def login_view(request):
    user = _get_user_info(request)
    if user and not user.is_anonymous():
        return dashboard(request)

    else:
        from django.contrib.auth import authenticate, login

        if 'username' in request.POST:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('dash')
                else:
                    # Return a 'disabled account' error message
                    pass
            else:
                # Return an 'invalid login' error message.
                pass

        from .forms import LoginForm
        login_form = LoginForm()

        return render(request,'login.html',{'user':user, 'form':login_form})


def _search_query_constructor(request):
    m_query = {}
    # putting queryset in session is inflexible, disabled for now
    # if 'query_set' in request.session:
    #     m_query = request.session['query_set']
    # else:
    #     request.session['query_set'] = {}
    # get unique product ids that contains keyword search
    data = PubTechProdResult.objects.all()

    param_map = {
        'q':'keywords',
        't':'technique',
        'company':'supplier',
        'target_human':'target-human',
        'target_mouse':'target-mouse',
        'host':'host'
    }


    for k,v in param_map.items():
        if k in request.GET:
            m_query[v] = request.GET[k]

    if 'keywords' in m_query:
        kw = m_query['keywords']
        if kw:
            cat_ids = _get_catids_from_q(kw)
            if cat_ids:
                data = data.filter(prod_id__in=cat_ids)
            elif type(cat_ids) is list and len(cat_ids) == 0:
                data = []

            if 'kw_history' not in request.session:
                request.session['kw_history'] = [kw]
            else:
                hist = request.session['kw_history']
                print hist

                if kw in hist:
                    hist.insert(0, hist.pop(hist.index(kw)))
                else:
                    hist.insert(0, kw)

                if len(hist) > 7:
                    hist = hist[:7]
                request.session['kw_history'] = hist

    if 'technique' in m_query:
        tech_name = m_query['technique']
        if tech_name:
            data = data.filter(technique_group=tech_name)

    if 'supplier' in m_query:
        supplier = m_query['supplier']
        if supplier:
            data = data.filter(supplier=supplier)

    if 'host' in m_query:
        host = m_query['host']
        if host:
            data = data.filter(prod__host=host)

    if 'target-human' in m_query:
        data = data.filter(prod__reactivity_human=1)

    if 'target-mouse' in m_query:
        data = data.filter(prod__reactivity_mouse=1)

    return (m_query, data)

@login_required
def dashboard(request):
    from datetime import date
    user = _get_user_info(request)
    if not user or user.is_anonymous():
        return redirect('login')

    pass_data = {'user': user}

    q_input, data = _search_query_constructor(request)
    pass_data['query_set'] = q_input
    tech_data = []
    cite_pass = []
    if data:
        tech_name_group = 'technique_group'
        tech_stats = data.values(tech_name_group).annotate(Count(tech_name_group)).order_by(tech_name_group)

        for i in tech_stats:
            ks = i.keys()
            tech_data.append([str(i[ks[0]]),i[ks[1]]])

        catids = []
        if 'keywords' in q_input:
            catids = _get_catids_from_q(q_input['keywords'])

        sql = """
        SELECT `pub_tech_prod_result`.`technique_group`, year(`scin_pub_meta`.`pub_date`) AS `pub_year`, COUNT(*) AS `cite_count`
        FROM `pub_tech_prod_result` INNER JOIN `scin_pub_meta` ON ( `pub_tech_prod_result`.`doc_id` = `scin_pub_meta`.`id` )
        """

        if type(catids) is list and len(catids) > 0:
            sql += " WHERE (`pub_tech_prod_result`.`prod_id` IN ( "
            sql += ','.join(str(id) for id in catids)
            sql += ")) "

        sql += "GROUP BY `pub_year`,`pub_tech_prod_result`.`technique_group` ORDER BY `pub_tech_prod_result`.`technique_group`,`pub_year` ASC"
        print sql
        from django.db import connections
        with connections['search_db'].cursor() as cursor:
            cursor.execute(sql)
            qres = [i for i in cursor.fetchall()]

        if qres:
            #qs = data.filter(doc__pub_date__lte=date.today())
            #qs = data.extra(select={'pub_year' : 'year(pub_date)'})
            #cite_stats = qs.values('pub_year', 'technique_group').annotate(Count('pub_year')).order_by('technique_group')
            import pandas as pd
            cite_df = pd.DataFrame(qres, columns=['technique', 'year', 'citations'])
            cite_df = cite_df.pivot(index='technique', columns='year', values='citations')
            #cite_df = cite_df.fillna(0)

            cite_data = [['year']+[str(i) for i in cite_df.index.values]] + list(cite_df.T.itertuples())
            cite_data = [list(i) for i in zip(*cite_data)]

            from django.http import JsonResponse
            cite_json = JsonResponse(cite_data, safe=False)
            cite_pass = cite_json.content
        else:
            cite_pass = []
    pass_data['tech_data'] = tech_data
    pass_data['cite_data'] = cite_pass
    pass_data['request'] = request.GET
    return render(request, "search/dashboard.html", pass_data)

@login_required
def index(request):
    user = _get_user_info(request)
    if not user or user.is_anonymous():
        return redirect('login')

    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

    pass_data = {'user':user}

    q_input, data = _search_query_constructor(request)
    pass_data['query_set'] = q_input


    # data = data.values('figure__url', 'figure__header','figure__content',
    #     'doc__title', 'technique_group', 'doc__publisher','doc__src_address',
    #     'doc__pdf_address','supplier', 'product_name').annotate(Count('figure__url')).order_by('doc__title', 'figure__figure_id')

    prod_data = data.values('prod_id').annotate(num_docs=Count('doc_id')).order_by('-num_docs')
    #data = data.order_by('-doc__citation','doc__title', 'figure__header')

    pagi = Paginator(prod_data, 10)
    page = request.GET.get('page')
    try:
        pdata = pagi.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        pdata = pagi.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        pdata = pagi.page(pagi.num_pages)

    obj_data = []
    for i in pdata:
        print i
        entry = { 'num_docs': i['num_docs'] }
        pid = i['prod_id']
        entry['info'] = PubProductInfo.objects.get(pk=pid)

        figs = PubTechProdResult.objects.filter(prod_id=pid, technique_group=q_input['technique'], is_shown=True).values('figure__url', 'figure_id', 'figure__header','figure__doc__citation').annotate(num_sentence=Count('sentence')).order_by('-figure__doc__citation','-num_sentence')
        entry['figures'] = figs
        obj_data.append(entry)

    pass_data['data'] = obj_data
    pass_data['pagi'] = pdata

    from .forms import SearchFilterForm
    filter_form = SearchFilterForm(data, data=request.GET, auto_id=False)
    pass_data['filter_form'] = filter_form

    # suppliers = data.values('supplier').annotate()
    # pass_data['suppliers'] = suppliers

    # hosts = data.values('prod__host').annotate()
    # pass_data['hosts'] = hosts

    return render(request, "search/index.html", pass_data)


@login_required
def view(request, id):
    user = _get_user_info(request)
    if not user or user.is_anonymous():
        return redirect('login')
    pass_data = {'user':user}

    from search.models import PubProductInfo, PubProductResult, ScinPubFigure

    pinfo = PubProductInfo.objects.filter(pk=id)[0]
    pass_data['pinfo'] = pinfo

    docs = PubTechProdResult.objects.filter(prod_id=id).values('doc__title', 'doc__author', 'doc__pub_date','doc__src_address', 'doc__pdf_address',
        'doc__publisher', 'doc__doc_id', 'technique_group', 'doc__citation').distinct().order_by('-doc__citation')
    pass_data['docs'] = docs

    figures = PubTechProdResult.objects.filter(prod_id=id).values('doc__title', 'doc__citation','doc__pub_date','doc__publisher','figure_id',
        'figure__url', 'figure__header', 'technique_group').distinct().order_by('-doc__citation', 'figure__header')
    pass_data['figures'] = figures

    return render(request, "search/view.html", pass_data)

@login_required
def figure_view(request, id):
    from django.template.loader import render_to_string

    fig = ScinPubFigure.objects.filter(pk=id)[0]
    passdata = {'figure':fig}
    if request.is_ajax():
        html = render_to_string('search/figure_modal.html', passdata)
        return HttpResponse(html)
    else:
        return render(request, "search/figure_view.html", passdata)



