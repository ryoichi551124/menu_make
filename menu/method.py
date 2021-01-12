import numpy as np
import pandas as pd
import random
import csv
import fcntl
import shutil
import pickle
import lightgbm as lgb
from . import features


with open('rakuten_main.csv') as f:
    reader = csv.DictReader(f)
    main = [row for row in reader]

with open('rakuten_sub.csv') as f:
    reader = csv.DictReader(f)
    sub = [row for row in reader]

with open('rakuten_soup.csv') as f:
    reader = csv.DictReader(f)
    soup = [row for row in reader]

with open("menu_ai.pickle", mode="rb") as f:
    model = pickle.load(f)

not_soup_list = ['鍋', 'ラーメン', 'うどん', '蕎麦', '素麺', 'ハヤシライス',
                'つけ麺', 'おでん', 'クリームシチュー', 'ビーフシチュー',
                '坦々麺', '冷麺', 'ちゃんぽん', 'スープカレー']


def main_random():
    main_num_1 = random.randint(0, len(main)-1)
    main_num_2 = random.randint(0, len(main)-1)
    main_num_3 = random.randint(0, len(main)-1)
    main_num_4 = random.randint(0, len(main)-1)
    main_num_5 = random.randint(0, len(main)-1)
    main_num_6 = random.randint(0, len(main)-1)
    main_num_7 = random.randint(0, len(main)-1)
    main_num_8 = random.randint(0, len(main)-1)
    main_num_9 = random.randint(0, len(main)-1)

    params = {
        'main_num_1': main_num_1,
        'main_num_2': main_num_2,
        'main_num_3': main_num_3,
        'main_num_4': main_num_4,
        'main_num_5': main_num_5,
        'main_num_6': main_num_6,
        'main_num_7': main_num_7,
        'main_num_8': main_num_8,
        'main_num_9': main_num_9,

        'main_image_1': main[main_num_1]['foodImageUrl'],
        'main_image_2': main[main_num_2]['foodImageUrl'],
        'main_image_3': main[main_num_3]['foodImageUrl'],
        'main_image_4': main[main_num_4]['foodImageUrl'],
        'main_image_5': main[main_num_5]['foodImageUrl'],
        'main_image_6': main[main_num_6]['foodImageUrl'],
        'main_image_7': main[main_num_7]['foodImageUrl'],
        'main_image_8': main[main_num_8]['foodImageUrl'],
        'main_image_9': main[main_num_9]['foodImageUrl'],

        'main_name_1': main[main_num_1]['recipeTitle'],
        'main_name_2': main[main_num_2]['recipeTitle'],
        'main_name_3': main[main_num_3]['recipeTitle'],
        'main_name_4': main[main_num_4]['recipeTitle'],
        'main_name_5': main[main_num_5]['recipeTitle'],
        'main_name_6': main[main_num_6]['recipeTitle'],
        'main_name_7': main[main_num_7]['recipeTitle'],
        'main_name_8': main[main_num_8]['recipeTitle'],
        'main_name_9': main[main_num_9]['recipeTitle'],

        'main_description_1': main[main_num_1]['recipeDescription'],
        'main_description_2': main[main_num_2]['recipeDescription'],
        'main_description_3': main[main_num_3]['recipeDescription'],
        'main_description_4': main[main_num_4]['recipeDescription'],
        'main_description_5': main[main_num_5]['recipeDescription'],
        'main_description_6': main[main_num_6]['recipeDescription'],
        'main_description_7': main[main_num_7]['recipeDescription'],
        'main_description_8': main[main_num_8]['recipeDescription'],
        'main_description_9': main[main_num_9]['recipeDescription'],
    }
    return params

#選んだ主菜を表示
def next_choice(main_num):
    main_image = main[int(main_num)]['foodImageUrl']
    main_name = main[int(main_num)]['recipeTitle']
    main_description = main[int(main_num)]['recipeDescription']

    params = {
        'main_num': main_num,
        'main_image': main_image,
        'main_name': main_name,
        'main_description': main_description,
    }
    return params


def menu_predict(main_num):
    main_num = int(main_num)
    sub_num_list = []
    soup_num_list = []
    soup_num = 0

    #空のファイルをコピーしてtrain.csvを初期化
    shutil.copyfile("empty.csv", "train.csv")

    #鍋や麺類の場合は汁物をなしにする
    for not_soup in not_soup_list:
        if not_soup in main[main_num]['recipeTitle']:
            soup_num = 260

    #train.csvを開いてロックする
    with open('train.csv', 'r+') as f:
        fcntl.flock(f.fileno(), fcntl.LOCK_EX)
        reader = csv.reader(f)
        train = [row for row in reader]
        writer = csv.writer(f, lineterminator='\n')

        #副菜と汁物のランダムな組み合わせを取得
        for i in range(3000):
            #ランダムな組み合わせのデータ1列を作る
            with open('combi.csv') as ff:
                reader = csv.DictReader(ff)
                combi = [row for row in reader]

            sub_num = random.randint(0, len(sub)-1)
            if soup_num != 260:
                soup_num = random.randint(0, len(soup)-2)

            all_list = list(combi[0].keys())[7:]

            combi[0]['主菜'] = main[main_num]['recipeTitle']
            combi[0]['副菜'] = sub[sub_num]['recipeTitle']
            combi[0]['汁物'] = soup[soup_num]['recipeTitle']
            combi[0]['主菜ID'] = main[main_num]['recipeId']

            for material in all_list:
                if material in main[main_num]['recipeMaterial']:
                    combi[0][material] = 1  
                if material in sub[sub_num]['recipeMaterial']:
                    combi[0][material] = 1  
                if material in soup[soup_num]['recipeMaterial']:
                    combi[0][material] = 1  

            combi[0]['main_genre'] = main[main_num]['genre']
            combi[0]['sub_genre'] = sub[sub_num]['genre']
            combi[0]['soup_genre'] = soup[soup_num]['genre']

            #作成した1列のデータをtrain.csvに追加する
            writer.writerow(combi[0].values())
        #train.csvのロックを解除
        f.flush()
        fcntl.flock(f.fileno(), fcntl.LOCK_UN)


    #train.csvをpandasで読み込む
    train = pd.read_csv('train.csv', index_col=0)
    train.reset_index(drop=True, inplace=True)

    #main_genreのonehot
    add_columns = pd.DataFrame(np.zeros(4).reshape(1, 4), columns=['main_genre_1', 'main_genre_2', 'main_genre_3', 'main_genre_4'])
    for i in add_columns:
        train[i] = 0
    train.drop('main_genre', axis=1, inplace=True)
    main_genre_get = 'main_genre_' + main[main_num]['genre']
    train[main_genre_get] = 1
    
    #sub_genreのonehot
    train = pd.get_dummies(train, columns=['sub_genre'])

    #soup_genreのonehot
    #データの中に汁なしがあるかどうか
    if 0 not in train['soup_genre']:
        train = pd.get_dummies(train, columns=['soup_genre'])
    elif 0 in train['soup_genre']:
        train['soup_genre_0'] = 1 
        train[['soup_genre_1', 'soup_genre_2', 'soup_genre_3', 'soup_genre_4']] = 0
        train.drop('soup_genre', axis=1, inplace=True)

    train['genre_total_1'] = train['main_genre_1'] + train['sub_genre_1'] + train['soup_genre_1']
    train['genre_total_2'] = train['main_genre_2'] + train['sub_genre_2'] + train['soup_genre_2']
    train['genre_total_3'] = train['main_genre_3'] + train['sub_genre_3'] + train['soup_genre_3']
    train['genre_total_4'] = train['main_genre_4'] + train['sub_genre_4'] + train['soup_genre_4']

    train_origin = train.copy(deep=True)

    #trainファイルの確認
    #train.to_csv('test.csv')

    #特徴量の追加
    train = features.features(train)

    train.drop(['ID', '主菜', '副菜', '汁物', '主菜ID', '採用/不採用'], axis=1, inplace=True)

    #モデルを使って予想
    pred = model.predict_proba(train)
    pred_sort_index = np.argsort(pred[:, 0])
    print(np.abs(np.sort(-pred[:, 1]))[:10])

    #上位50件の副菜、汁物の名前リスト
    sub_name_list = []
    soup_name_list = []
    for i in range(80):
        sub_name = train_origin.iloc[pred_sort_index[i]]['副菜']
        sub_name_list.append(sub_name)
        #副菜重複削除
        sub_name_list = sorted(set(sub_name_list), key=sub_name_list.index)
        soup_name = train_origin.iloc[pred_sort_index[i]]['汁物']
        soup_name_list.append(soup_name)
        #汁物重複削除
        if soup_name_list[0] != 'なし':
            soup_name_list = sorted(set(soup_name_list), key=soup_name_list.index)
    print('len(sub_name_list):', len(sub_name_list))
    print('len(soup_name_list):', len(soup_name_list))

    params = {
        'main_num': main_num,
        'sub_name_list': sub_name_list,
        'soup_name_list': soup_name_list,
    }
    return params


def recipe_info(main_num, sub_name_list, soup_name_list, count):
    count = int(count)
    main_num = int(main_num)

    main_image = main[main_num]['foodImageUrl']
    main_name = main[main_num]['recipeTitle']
    main_description = main[main_num]['recipeDescription']
    main_url = main[main_num]['recipeUrl']

    sub = pd.read_csv('rakuten_sub.csv', index_col=0)
    soup = pd.read_csv('rakuten_soup.csv', index_col=0)

    sub = sub[sub['recipeTitle'] == sub_name_list[count]]
    sub_name = sub_name_list[count]
    sub_image = sub.iloc[0]['foodImageUrl']
    sub_description = sub.iloc[0]['recipeDescription']
    sub_url = sub.iloc[0]['recipeUrl']

    soup = soup[soup['recipeTitle'] == soup_name_list[count]]
    soup_name = soup_name_list[count]
    soup_image = soup.iloc[0]['foodImageUrl']
    soup_description = soup.iloc[0]['recipeDescription']
    soup_url = soup.iloc[0]['recipeUrl']

    params = {
        'main_num': main_num,
        'main_image': main_image,
        'main_name': main_name,
        'main_description': main_description,
        'main_url': main_url,
        'sub_name': sub_name,
        'sub_image': sub_image,
        'sub_description': sub_description,
        'sub_url': sub_url,
        'soup_name': soup_name,
        'soup_image': soup_image,
        'soup_description': soup_description,
        'soup_url': soup_url,
    }
    return params
