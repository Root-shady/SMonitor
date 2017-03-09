from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from system.models import Menu

def paginate_data(request, data_set, data_serializer):
    context = {}
    page = request.GET.get('page', 1)
    num = request.GET.get('num', 10)
    try:
        page = int(page)
        num= int(num)
    except Exception:
        page = 1
        num = 10
    if num == 0:
        num = data_set.count()
    paginator = Paginator(data_set, num)
    try:
        data_set = paginator.page(page)
    except PageNotAnInteger:
        data_set = paginator.page(1)
    except EmptyPage:
        data_set = paginator(paginator.num_pages)
    serializer = data_serializer(data_set, many=True)
    context['records'] = serializer.data
    context['count'] = paginator.count
    context['num_pages'] = paginator.num_pages
    return context

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def format_response(context, success, data, error=None):
    context['status'] = success
    if error:
        context['retErr'] = error
    context['retData'] = data


def form_structure(origin):
    result = []
    for item in origin:
        if item['pid'] == 0:
            result.append(item)
        else:
            add_child(item, result)
    return result

def add_child(item, result):
    for temp in result:
        if item['pid'] == temp['id']:
            temp.setdefault('child', [])
            temp['child'].append(item)
        elif 'child' in temp:
            add_child(item, temp['child'])
        else:
            pass

def nest_sort(origin):
    for index in range(len(origin)-1):
        if 'child' in origin[index]:
            nest_sort(origin[index]['child'])
    origin.sort(key=lambda k:k['sort'])

def get_user_menu(user):
    menus = Menu.objects.filter(is_visible=1).values('id', 'title', 'selected', 'level', 'url', 'pid', 'sort')
    for menu in menus:
        if not menu['pid']:
            menu['pid'] = 0
    menus = sorted(menus, key=lambda k: k['pid'])
    temp = form_structure(menus)
    nest_sort(temp)
    return temp



