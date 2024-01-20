#ライブラリーのインポート
from bs4 import BeautifulSoup
import re
import requests
from time import sleep
import pandas as pd
from urllib.parse import urljoin
import sqlite3
import pandas as pd
import os




#変数urlにSUUMOホームページのURLを格納する
#東京都23区
#家賃10万〜30万
#1LDK, 2K, 2DK, 2LDK, 3K, 3DK, 3LDK
#マンション
#駅徒歩20分以内
#築年数30年以内
url = 'https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&bs=040&pc=30&smk=&po1=25&po2=99&shkr1=03&shkr2=03&shkr3=03&shkr4=03&sc=13101&sc=13102&sc=13103&sc=13104&sc=13105&sc=13113&sc=13106&sc=13107&sc=13108&sc=13118&sc=13121&sc=13122&sc=13123&sc=13109&sc=13110&sc=13111&sc=13112&sc=13114&sc=13115&sc=13120&sc=13116&sc=13117&sc=13119&ta=13&cb=10.0&ct=30.0&md=04&md=05&md=06&md=07&md=08&md=09&md=10&ts=1&et=20&mb=0&mt=9999999&cn=30&fw2=&page={}'
#'Requests'を使って1で設定したURLにアクセスする
res = requests.get(url.format(1))
#取得したHTMLを'BeautifulSoup'で解析する
soup_total_page = BeautifulSoup(res.text, 'html.parser')
#最後のPage数を取得する
last_page = int(soup_total_page.find('ol', class_='pagination-parts').find_all('li')[-1].text)

#変数d_listにからのリストを作成する
d_list = []

#1〜3をループする
#for i in tqdm(range(1, 3)):
#最後のページまでを取得する
#for i in tqdm(range(1, last_page+1)):
#tqdmは.pyでは使用できない

for i in range(1, 3):

    
    print('d_listの大きさ:', len(d_list))
    
    #変数target_urlに、アクセスさくのURLを格納する
    target_url = url.format(i)
    #print()してtarget_urlを確認する
    print(target_url)
    
    #2. 'Requests'を使って1で設定したURLにアクセスする
    r = requests.get(target_url)
    
    #requestsの間隔を1秒あける
    sleep(1)

    #3. 取得したHTMLを'BeautifulSoup'で解析する
    soup = BeautifulSoup(r.text, 'html.parser')

    #4. 全ての物件情報(20件)を取得する。
    contents = soup.find_all('div', class_='cassetteitem')
    
    #5. 各物件情報から『物件の詳細』と『各部屋の情報』
    #各物件情報をforループで取得する。
    for content in contents:
        #6. 物件情報と部屋情報を取得しておく
        #物件情報を変数detailに格納する
        #各部屋の情報を変数tableに格納する
        detail = content.find('div', class_='cassetteitem-detail')
        table = content.find('table', class_='cassetteitem_other')
    
        #物件情報から必要な情報を取得する。
        #変数titleに物件名を格納する
        #変数propery_photoに物件画像のurlを格納する
        #変数addressに住所を格納する
        #変数accessにアクセス情報を格納する
        #変数age_building_floorsに築年数と建物の階数を格納する
        title = detail.find('div', class_='cassetteitem_content-title').text
        # detail変数からimgタグを検索
        img_tag = detail.find('img', class_='js-noContextMenu js-linkImage js-scrollLazy js-adjustImg')

        # imgタグが存在し、rel属性を持っている場合、その値を取得
        property_photo = img_tag['rel'] if img_tag and img_tag.has_attr('rel') else '画像のURLが見つかりません'

        # property_photo変数には画像のURLが格納される

        
        address = detail.find('li', class_='cassetteitem_detail-col1').text
        access = detail.find('li', class_='cassetteitem_detail-col2')
        age_building_floors = detail.find('li', class_='cassetteitem_detail-col3')
        
        #accessについて詳細に情報を取得していく
        #access要素内のすべてのdivタグを取得
        access_divs = access.find_all('div')
        
        
        # 路線名と駅名を取得する正規表現パターン
        station_pattern = r'(.+?/.*?駅)'
        # 数字のみを抽出する正規表現パターン
        pattern = r'\d+'

        # 各最寄駅の情報を格納するためのリスト
        stations = []
        times = []

        # access要素内のすべてのdivタグを取得し、ループ処理
        for access_div in access.find_all('div')[:3]:  # 最初の3つのdivタグのみを対象
            access_text = access_div.text

            # 駅名を抽出
            station_match = re.search(station_pattern, access_text)
            if station_match:
                station = station_match.group(1) + '駅'
            else:
                station = None

            # 最寄駅からの時間を抽出
            time_match = re.search(pattern, access_text)
            if time_match:
                time = int(time_match.group())
            else:
                time = 0

            # 結果をリストに追加
            stations.append(station)
            times.append(time)

        # 最寄駅名と時間の情報を変数に展開
        access_1_station, access_2_station, access_3_station = stations
        access_1_time, access_2_time, access_3_time = times
         
        #age_building_floors要素内のすべてのdivタグを取得
        age_building_floors_divs = age_building_floors.find_all('div')

        # 築年数age_textと建物の階数building_floors_textのテキストを取得
        age_text = age_building_floors_divs[0].text 
        building_floors_text = age_building_floors_divs[1].text 
        
        #数字のみを抽出する正規表現パターン
        pattern = r'\d+'
        #築年数から数字を抽出
        age = re.search(pattern, age_text)
        if age:
            age = age.group()
        #建物の階数から数字を抽出
        building_floors = re.search(pattern, building_floors_text)
        if building_floors:
            building_floors = building_floors.group()
    
        #部屋情報のブロックから各部屋情報を取得する
        #変数tableから全てのtrタグを取得して、変数tr_tagsに格納
        #tr_tagsの中から最初の1つだけtr_tagに格納
        tr_tags = table.find_all('tr', class_='js-cassette_link')
        tr_tag = tr_tags[0]
    
        #各部屋情報をforループで取得する
        for tr_tag in tr_tags:
        
            #部屋情報の行から、欲しい情報を取得する
            #変数floor, price, first_fee, capacityに4つの情報を格納する
            floor_number, price, first_fee, capacity = tr_tag.find_all("td")[2:6]
            #さらに細かい情報を取得する
            #priceは賃料(fee)と管理費(management_fee)
            #first_feeは敷金(deposit)と礼金(qratuity)
            #capacityは間取り(madori)と専有面積(menseki)
            rent_price, manegement_fee_price = price.find_all('li')
            deposit_price, qratuity_price = first_fee.find_all('li')
            madori_capacity, menseki_capacity = capacity.find_all('li')
            
            #テキストデータを取得する
            floor_text = floor_number.text
            rent_text = rent_price.text
            manegement_fee_text = manegement_fee_price.text
            deposit_text = deposit_price.text
            qratuity_text = qratuity_price.text
            madori = madori_capacity.text
            menseki_text = menseki_capacity.text
            
            #数字のみを抽出する正規表現パターン
            pattern = r'\d+'
            
            # 小数を含む数値にマッチする正規表現パターン
            pattern2 = r'\d+(\.\d+)?'
            
            #階数floor_textから数字を抽出
            #int型にして、階数floorに格納する。
            floor = re.search(pattern, floor_text)
            if floor:
                floor = int(floor.group())
            
            #管理費manegement_fee_textから数字を抽出
            #int型にして、管理費manegement_fee_textに格納する。
            manegement_fee = re.search(pattern, manegement_fee_text)
            if manegement_fee:
                manegement_fee = int(manegement_fee.group())
            else:
                manegement_fee = 0  # 管理費が取得できない場合は0円とする

            
            
            #面積mensekiから数字を抽出
            #float型にして、面積mensekiに格納する。
            menseki = re.search(pattern2, menseki_text)
            if menseki:
                menseki = float(menseki.group())
        
            #数字（整数または小数）を抽出する正規表現パターン
            pattern3 = r'(\d+(\.\d+)?)万'
            
            # 金額を円単位に変換する関数
            def convert_to_yen(text):
                # '万'単位の金額を探す
                match = re.search(pattern3, text)
                if match:
                    # 数字部分を取得し、float型に変換してから10000を乗算
                    number = float(match.group(1))
                    return int(number * 10000)
                else:
                    #'万'がない場合は通常の数字を探す
                    match = re.search(r'\d+', text)
                    if match:
                        return int(match.group())
                    else:
                        # 数字が見つからない場合は0や適切なデフォルト値を返す
                        return 0                
            # 各テキストから金額を円単位で抽出
            rent = convert_to_yen(rent_text)
            deposit = convert_to_yen(deposit_text)
            qratuity = convert_to_yen(qratuity_text)
            
            # ベースURLを定義する
            base_url = 'https://suumo.jp'

            # 物件の詳細ページへのリンクを取得する
            a_tag = tr_tag.find('a', class_='js-cassette_link_href cassetteitem_other-linktext')
            relative_url = a_tag['href'] if a_tag else None

            # 相対URLを完全なURLに変換する
            if relative_url:
                url_site = urljoin(base_url, relative_url)
            else:
                url_site = 'リンクが見つかりません'

            # url_siteは完全なURLを含む

        
            #取得した全ての情報を辞書に格納する
            #変数dにこれまで取得した11項目を辞書に格納する
            
            d = {
                "Property Name": title, 
                "Property Photo": property_photo,
                "Address": address,
                "Access": access,
                "Nearest Station 1": access_1_station,
                "Time to Nearest Station 1 (min)": access_1_time,
                "Nearest Station 2": access_2_station,
                "Time to Nearest Station 2 (min)": access_2_time,
                "Nearest Station 3": access_3_station,
                "Time to Nearest Station 3 (min)": access_3_time,
                "Building Age (years)": age,
                "Building Floors": building_floors,
                "Floor Number": floor,
                "Rent (Yen)": rent,
                "Maintenance Fee (Yen)": manegement_fee,
                "Deposit (Yen)": deposit,
                "Key Money (Yen)": qratuity,
                "Layout": madori,
                "Area (m2)": menseki,
                "URL": url_site,
            }
        
            #取得した辞書をd_listに格納する
            d_list.append(d)
            
#変数d_listを使って、データフレームを作成する
df = pd.DataFrame(d_list)

# この関数はDataFrameの各セルをクリーニングするために使用されます
def clean_text(cell):
    # セルがNoneの場合、変更せずにそのまま返します
    if cell is None:
        return cell

    # セルが文字列型の場合、改行、キャリッジリターン、タブをスペースに置換して返します
    if isinstance(cell, str):
        return re.sub('[\n\r\t]', ' ', cell)

    # セルがBeautifulSoupのTagオブジェクトの場合（HTMLタグ）、
    # そのテキスト内容を取得し、同様に置換して返します
    elif hasattr(cell, 'text'):
        return re.sub('[\n\r\t]', ' ', cell.text)

    # 上記の条件に当てはまらない場合、セルをそのまま返します
    else:
        return cell

# DataFrameの各セルに対してclean_text関数を適用します
df2 = df.applymap(clean_text)

#住所、家賃、階が一致した物件を重複物件とみなし、重複した行を特定する条件を指定
duplicate_condition = df2.duplicated(subset=['Address', 'Rent (Yen)', 'Floor Number', 'Layout', 'Area (m2)',], keep=False)

# 重複した行を抽出
duplicates = df2[duplicate_condition]

# 重複した行を削除
df3 = df2.drop_duplicates(subset=['Address', 'Rent (Yen)', 'Floor Number', 'Layout', 'Area (m2)',], keep='first')

# SQLiteデータベースファイルを作成（または既存のものに接続）
# スクリプトのあるディレクトリの絶対パスを取得
script_dir = os.path.dirname(os.path.abspath(__file__))

# データベースファイルへの絶対パスを生成
db_path = os.path.join(script_dir, 'Tokyo23_RealEatate_DB.db')

# データベースへの接続
conn = sqlite3.connect(db_path)

# df3は以前に作成されたPandasのデータフレーム
# このデータフレームを'table_name'という名前のテーブルに転送
# 存在しない場合は新規作成、存在する場合は置き換える
df3.to_sql('Tokyo_23', conn, if_exists='replace', index=False)

# データベースの接続を閉じる
conn.close()