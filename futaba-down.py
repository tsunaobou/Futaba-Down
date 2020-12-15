#Futaba-down v1.02

import requests
import re
from bs4 import BeautifulSoup
import urllib.request
import os.path
import os
from time import sleep

#URL入力
name = input("ダウンロードしたいスレのURLを入力:")

#後で使うためにスレのURLを少し加工して持っておく
name2 = re.match(r'https.*?net',name)
#↓ここでname2でマッチングされた文字列をheadとして取得しておく
head = name2.group()

#getリクエスト実行
response = requests.get(name)
#3秒スリープ
print("3秒wait中")
sleep(3)

#beautifulsoupでHTMLをパース
soup = BeautifulSoup(response.content,'html.parser')

#後で使うためにtitleタグを抽出
pagetitle = soup.title.text

#aタグのhref要素を抽出
geturl = [tag.get('href') for tag in soup('a')]

#被りがあるので重複を削除し再リスト化
duplicate_delete = list(set(geturl))

'''
ここで万が一スレの誰かがjpgやpngなどのキーワードが含まれかつ画像ファイルでないもののURLを貼ったらそれもaタグhref属性としてみなされてしまい、
ダウンロードの際に例外が発生してしまう　そのため、その場合に含まれるjump.phpが配列の中にあるかどうか検索し、当てはまらなかったものだけを
それ以外を再度別の配列に格納するという動作を行い確実性を担保する。
'''

rejudge = [redo for redo in duplicate_delete if 'jump.php' not in redo]


#それぞれの拡張子を含むアドレスだけを抽出した配列を６つ作成
#これは正規表現でやるのが面倒だったからと言う理由もある。
jpgget = [feature for feature in rejudge if 'jpg' in feature]
pngget = [feature for feature in rejudge if 'png' in feature]
webmget = [feature for feature in rejudge if 'webm' in feature]
mp4get = [feature for feature in rejudge if 'mp4' in feature]
gifget = [feature for feature in rejudge if 'gif' in feature]
webpget = [feature for feature in rejudge if 'webp' in feature]

#配列を合成して一つにする
download_list = jpgget+pngget+webmget+webpget+mp4get+gifget

#一つにした配列に最初に作ったアドレスの頭の部分を連結してダウンロード可能なURL形式へ 結果は配列で出てくる
download_ready = list(map(lambda x: head + x,download_list))
#ダウンロードする個数を数える
download_number = len(download_list)

#ダウンロード前のフォルダ作成、移動
os.makedirs(pagetitle,exist_ok=True)
os.chdir(f"{pagetitle}")

#ダウンロードパート
for count,url in enumerate(download_ready,1):

    filename= os.path.basename(url)
    urllib.request.urlretrieve(url,filename)
    #進捗状況を表現
    print(f"{download_number}個中{count}個のダウンロード完了 2秒wait中")
    #スリープを一回ごとに2sec挟む
    sleep(2)


print(f"{download_number}個のメディアのダウンロードが完了しました！")