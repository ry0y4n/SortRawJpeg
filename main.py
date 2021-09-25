from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth

import os

#Googleサービスを認証
gauth = GoogleAuth()

#資格情報ロードするか、存在しない場合は空の資格情報を作成
gauth.LoadCredentialsFile("mycreds.txt")

#Googleサービスの資格情報がない場合
if gauth.credentials is None:
    #ユーザーから認証コードを自動的に受信しローカルWebサーバーを設定
    gauth.LocalWebserverAuth()
#アクセストークンが存在しないか、期限切れかの場合    
elif gauth.access_token_expired:
    #Googleサービスを認証をリフレッシュする
    gauth.Refresh()
#どちらにも一致しない場合    
else:
    #Googleサービスを承認する
    gauth.Authorize()
#資格情報をtxt形式でファイルに保存する  
gauth.SaveCredentialsFile("mycreds.txt") 
       
#Googleドライブの認証処理
drive = GoogleDrive(gauth)

#RAFデータの拡張子を設定する
raw_ext = ".RAF"

#GoogleDrive上のフォルダIDを設定する
raw_folder_id = "1R-_sa3ZJXmYg0jyksCzBm2xKFJUBrZpu"
jpg_folder_id = "1FX_HoNHVfL8sIX0uSaNEWihW7v_qK1jD"

#アップロードしたいローカルフォルダのパスを入力させる
path = input("Enter your path: ")

print("Start Uploading...")

#for文によるループ処理（繰り返し処理）
for i, x in enumerate(os.listdir(path)):
    print("[{}/{}]".format(i + 1, len(os.listdir(path))))
    ext = os.path.splitext(x)[-1]
    #GoogleDriveFileオブジェクト作成
    f = drive.CreateFile({
        'title' : x,
        'parents': [{'kind': 'drive#fileLink', 'id': raw_folder_id if ext == raw_ext else jpg_folder_id}]
    })
    #ローカルのファイルをセットしてアップロード
    f.SetContentFile(os.path.join(path,x))
    #Googleドライブにアップロード
    f.Upload()

    f = None

print("Finish Uploading.")
