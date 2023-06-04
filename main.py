import glob
import os
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd

# 80KBを超えるファイルはバックアップを取って新規ファイルを作成する
MAX_FILE_SIZE = 80 * 1024

def get_last_id(file_name: str) -> int:
    """ tsvファイルの最後のid番号を取得する

    Args:
        file_name (str): tsvファイル名

    Returns:
        int: 最後のid番号
    """
    # tsvファイルが存在する場合は最後のid 番号を取得し、それ以外は0を代入しておく
    if os.path.exists(file_name):
        df = pd.read_csv(file_name, sep='\t')
        last_id: int = (df["id"].iloc[-1]) + 1
    else:
        last_id = 0

    return last_id

def scraping(url_list: list, last_id: int, now: datetime) -> list:
    """ スクレイピングする

    Args:
        url_list (list): スクレイピングするURLのリスト
        last_id (int): 最後のid番号
        now (datetime): 現在時刻

    Returns:
        list: スクレイピング結果のリスト
    """

    data: list = []
    # 各URLに対してリクエストを行い、HTMLを解析
    for url in url_list:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # ここでsoupオブジェクトを使用して必要な情報を取得...
        # この例では、URL自体が必要な情報として格納されます。
        tag_list = soup.select('a[href]')
        for tag in tag_list:
          get_url = tag.get('href')
          data.append({"id": last_id, "url": get_url, "create_at": now})
          last_id += 1

    return data

def convert_to_dataframe(data: list, file_name) -> pd.DataFrame:
  """ リストをデータフレームに変換して出力

  Args:
      data (list): リスト
      file_name ([type]): 出力するファイル名

  Returns:
      pd.DataFrame: データフレーム
  """
  df: pd.DataFrame = pd.DataFrame(data)
  df_len: int = len(df)

  for i in range(0, df_len, df_len):
      df_slice = df[i:i+df_len]

      if not os.path.exists(file_name):
        df_slice.to_csv(file_name, sep='\t', index=False, mode='a', encoding='utf-8')
      else:
        # last_id が 0 以外の場合はヘッダーを出力しない
        df_slice.to_csv(file_name, sep='\t', index=False, mode='a', encoding='utf-8' ,header=False)

  return df_slice


def upload_tsv():
    """boto3 を使って S3にアップロードする
    
    AWS CLI に情報を設定しておく必要がある
    
    """
    import boto3
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('bucket_name')
    bucket.upload_file('file_name', 'file_name')

    # AWS CLI に情報を設定しておく必要がある
    # aws configure
    







def concat_tsv(df: pd.DataFrame, file_list: list, join_file_name) -> None:
    """ tsvファイルを結合して重複urlを削除して出力

    Args:
        df (pd.DataFrame): 結合するデータフレーム
        file_list (list): 結合するファイルのリスト
        join_file_name (str): 結合したファイル名

    Returns:
        None
    """
    if file_list:
      df = pd.concat([pd.read_csv(f, sep='\t', encoding='utf-8') for f in file_list])
      df = df.drop_duplicates(subset="url")
      _backup_file(join_file_name, file_size=MAX_FILE_SIZE)
      df.to_csv(join_file_name, sep='\t', index=False)

def _backup_file(file_name: str, file_size=80) -> None:
    """ ファイルをバックアップする

    Args:
        file_name (str): ファイル名
        file_size (int, optional): ファイルサイズ. Defaults to 80.

    Returns:
        None
    """
    # ファイルサイズが大きくなると、重複チェックに時間がかかるため、新規ファイルを作成する
    if os.path.exists(file_name) and os.path.getsize(file_name) > file_size:
      # 元ファイルは、バックアップを取っておく
      back_file = f"{file_name}_{datetime.now().strftime('%Y%m%d%H%M%S')}.bak"
      os.rename(file_name, back_file)
      # bakファイルを圧縮する
      os.system(f"gzip {back_file}")

def match_file_name(dir_name: str, today: str) -> tuple:
    """ ファイル名を取得

    Args:
        dir_name (str): ディレクトリ名
        today (str): 今日の日付

    Returns:
        tuple: ファイル名とファイルリスト
    """

    # data/ 配下のファイル名が output_YYYYMMDD.tsv のファイルを取得
    file_name = f"{dir_name}output_{today}.tsv"
    # 'data/'ディレクトリ下のすべての'.tsv'ファイルを取得
    file_list = glob.glob(f"{dir_name}*.tsv")
    # 正規表現パターンを作成
    pattern = re.compile(re.escape(dir_name) + r'output_\d{8}.tsv')
    # パターンに一致するファイルだけを残す
    match_list = [f for f in file_list if pattern.match(f)]
    print('match_list: ', match_list)

    return file_name, match_list

def main():
    """ メイン関数 """
    # スクレイピングするウェブページのURLリストを想定
    url_list = [
      "http://example.com/1",
      "http://example.com/2",
      "http://example.com/3",
    ]
    now: datetime = datetime.now()
    today: str = now.date().strftime('%Y%m%d')
    dir_name: str = './data/'

    if not os.path.exists(dir_name):
      os.mkdir(dir_name)

    file_name, match_list = match_file_name(dir_name=dir_name, today=today)

    last_id = get_last_id(file_name)
    data = scraping(url_list, last_id, now)
    df = convert_to_dataframe(data, file_name)
    concat_tsv(
       df=df,
       file_list=match_list,
       join_file_name=f"{dir_name}output_join.tsv"
    )
    # match_list を削除
    for f in match_list:
      os.remove(f)

if __name__ == "__main__":
  main()
