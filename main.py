import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd


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

def concat_tsv(df: pd.DataFrame, file_list: list, join_file_name) -> None:
    """ tsvファイルを結合して重複urlを削除して出力

    Args:
        df (pd.DataFrame): 結合するデータフレーム
        file_list (list): 結合するファイルのリスト
        join_file_name (str): 結合したファイル名

    Returns:
        None
    """
    df = pd.concat([pd.read_csv(f, sep='\t', encoding='utf-8') for f in file_list])
    df = df.drop_duplicates(subset="url")
    df.to_csv(join_file_name, sep='\t', index=False)

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

    file_name = f"{dir_name}output_{today}.tsv"

    last_id = get_last_id(file_name)
    data = scraping(url_list, last_id, now)
    df = convert_to_dataframe(data, file_name)
    concat_tsv(df, file_list=[file_name], join_file_name=f"{dir_name}output_{today}_join.tsv")

if __name__ == "__main__":
  main()
