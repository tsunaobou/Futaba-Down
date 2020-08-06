#Futaba-down v1.01 

import requests
import re
from bs4 import BeautifulSoup
import urllib.request
import os.path
import os

#URL入力
name = input("ダウンロードしたいスレのURLを入力せよ。")

#後で使うためにスレのURLを少し加工して持っておく
name2 = re.match(r'https.*?net',name)
#↓ここでname2でマッチングされた文字列をheadとして取得しておく
#参考　https://note.nkmk.me/python-re-match-object-span-group/
head = name2.group()

#getリクエスト実行
response = requests.get(name)

#beautifulsoupでHTMLをパース
soup = BeautifulSoup(response.content,'html.parser')

#後で使うためにtitleタグを抽出
#参考　https://www.atmarkit.co.jp/ait/articles/1910/18/news015.html
pagetitle = soup.title.text

#aタグのhref要素を抽出
geturl = [tag.get('href') for tag in soup('a')]

#被りがあるので重複を削除し再リスト化
#参考　https://note.nkmk.me/python-list-unique-duplicate/
duplicate_delete = list(set(geturl))

'''
ここで万が一スレの誰かがjpgやpngなどのキーワードが含まれかつ画像ファイルでないもののURLを貼ったらそれもaタグhref属性としてみなされてしまい、
ダウンロードの際に例外が発生してしまう　そのため、その場合に含まれるjump.phpが配列の中にあるかどうか検索し、当てはまらなかったものだけを
それ以外を再度別の配列に格納するという動作を行い確実性を担保する。
'''

rejudge = [redo for redo in duplicate_delete if 'jump.php' not in redo]


#それぞれの拡張子を含むアドレスだけを抽出した配列を６つ作成
#これは正規表現でやるのが面倒だったからと言う理由もある。
#参考　https://note.nkmk.me/python-list-str-select-replace/
jpgget = [feature for feature in rejudge if 'jpg' in feature]
pngget = [feature for feature in rejudge if 'png' in feature]
webmget = [feature for feature in rejudge if 'webm' in feature]
mp4get = [feature for feature in rejudge if 'mp4' in feature]
gifget = [feature for feature in rejudge if 'gif' in feature]
webpget = [feature for feature in rejudge if 'webp' in feature]

#配列を合成して一つにする
download_list = jpgget+pngget+webmget+webpget+mp4get+gifget

#一つにした配列に最初に作ったアドレスの頭の部分を連結してダウンロード可能なURL形式へ 結果は配列で出てくる
#参考　https://it-engineer-lab.com/archives/122
download_ready = list(map(lambda x: head + x,download_list))
#ダウンロードする個数を数える
download_number = len(download_list)

#ダウンロード前のフォルダ作成
#参考　https://note.nkmk.me/python-save-file-at-new-dir/
os.makedirs(pagetitle,exist_ok=True)


#ダウンロードパート
for url in download_ready:

    filename= os.path.basename(url)
    urllib.request.urlretrieve(url,filename)

#埋め込み参考　https://note.nkmk.me/python-print-basic/
print('{}個のダウンロードが完了しました！'.format(download_number))