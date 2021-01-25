from django.shortcuts import render
from django.http import FileResponse
import random
from . import method

pred_sort_index =[]
sub_name_list = []
soup_name_list = []
count = 0


def index(request):
    return render(request, 'menu/start.html')

def start(request):
    params = method.main_random()
    return render(request, 'menu/index.html', params)

def next(request):
    main_num = list(request.POST.values())[1]
    params = method.next_choice(main_num)
    return render(request, 'menu/next.html', params)

def predict(request):
    global pred_sort_index, sub_name_list, soup_name_list, count
    #上位予想のメニューが頻出するためcountの初期化なし
    #count = 0

    #主菜のインデックスで副菜と汁物を予想
    main_num = request.POST['main_num']
    params = method.menu_predict(main_num)

    sub_name_list = params['sub_name_list']
    soup_name_list = params['soup_name_list']

    recipe_info = method.recipe_info(main_num, sub_name_list, soup_name_list, count)
    params.update(recipe_info)

    if params['soup_name'] != 'なし':
        return render(request, 'menu/result.html', params)
    elif params['soup_name'] == 'なし':
        return render(request, 'menu/result_nosoup.html', params)

def next_predict(request):
    global pred_sort_index, sub_name_list, soup_name_list, count

    count += 1
    if count >= len(sub_name_list) or count >= len(soup_name_list):
        count = 0
    print(len(sub_name_list))
    print(len(soup_name_list))
    print('count', count)
    params = method.recipe_info(request.POST['main_num'], sub_name_list, soup_name_list, count)
        
    if params['soup_name'] != 'なし':
        return render(request, 'menu/result.html', params)
    elif params['soup_name'] == 'なし':
        return render(request, 'menu/result_nosoup.html', params)




def loading(request):
    main_num = list(request.POST.values())[1]
    params = method.next_choice(main_num)
    return render(request, 'menu/loading.html', params)