import os
import sys
import time

try:
    import cv2
except:
    print("opencv-pythonライブラリがインストールされていません。\npip install opencv-pythonでインストールしてください。")
    a = input()
    sys.exit()

#ライブラリがインストールされているかチェックする
try:
    import requests
except:
    print("requestsライブラリがインストールされていません。\npip install requestsでインストールしてください。")
    a = input()
    sys.exit()

try:
    import tweepy
except:
    print("tweepyライブラリがインストールされていません。pip install tweepyでインストールしてください。")
    a = input()
    sys.exit()


CK="" #twitterのapiキー
CS="" #twitterのapi secretキー
AT="" #twitterのaccess tokenキー
AS="" #twitterのaccess token secretキー

#Twitterと接続。
auth = tweepy.OAuthHandler(CK, CS)
auth.set_access_token(AT, AS)
api = tweepy.API(auth)

new_dir_path = './icon/'

try:
    os.mkdir(new_dir_path)
except:
    pass

def gettwittericon(iconurl,path = "./icon/default.png"):

    #twieepyを使用して、ユーザーのスクリーンネームからアイコンのURLを取得する関数
    status=api.user_timeline(id=iconurl)[0]
    url = status.user.profile_image_url_https
    url2 = url.replace('normal','400x400')

    response = requests.get(url2)
    image = response.content
    with open(path, "wb") as f:
        f.write(image)
        print("ファイルをダウンロードしました。")    

    return url2

def main(verify = False):

    num = 0
    print(f"Twitterアイコン更新モード:{verify}")
    if verify == False:
        print("\n更新するにはTrueにしてください。")
    else:
        pass

    while True:
        me = api.me()
        print(gettwittericon(me.screen_name)) #me.screen_nameは自分のアカウントのscreen name
        img = cv2.imread("./icon/default.png")
        #高さを定義
        height = img.shape[0]                         
        #幅を定義
        width = img.shape[1]  
        #回転の中心を指定                          
        center = (int(width/2), int(height/2))
        #回転角を指定
        angle = 2.5
        #スケールを指定
        scale = 1.0
        #getRotationMatrix2D関数を使用
        trans = cv2.getRotationMatrix2D(center, angle , scale)
        #アフィン変換
        image2 = cv2.warpAffine(img, trans, (width,height))
        cv2.imwrite("./icon/default.png",image2)
        if (verify==True):
            api.update_profile_image("./icon/default.png")
        else:
            pass
        num = num + 1
        print(f"現在:{num}回目のループで、{angle*num}度回転しています。60秒後、また回転します。")
        time.sleep(60)
 
if __name__ == "__main__":
    main(True)
