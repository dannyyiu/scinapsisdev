from django import template

register = template.Library()

@register.filter
def author_format(value):
    return value
    if not value:
        return ''

    from django.utils.text import camel_case_to_spaces

    names = value.split(',')
    for i,n in enumerate(names):
        name = camel_case_to_spaces(n).split(' ')
        lastname = name[-1]
        init=''
        for j in range(len(name)-1):
            init += name[j][0].upper()
        fullname = init+' '+lastname.capitalize()
        names[i] = fullname
    return ', '.join(names)

@register.filter
def plosone_figure_url(value, size='medium'):
    if not value:
        return ''
    from urlparse import urlparse, parse_qs

    uri = urlparse(value)
    dict = parse_qs(str(uri.query))
    id_str = dict['id'][0]
    print '#',id_str
    fig_size = 'PNG_M'
    if size=='small':
        fig_size = 'PNG_S'
    elif size=='large':
        fig_size = 'PNG_L'
    plos_url = 'http://www.plosone.org/article/fetchObject.action?representation='+fig_size+'&uri='+id_str
    return plos_url