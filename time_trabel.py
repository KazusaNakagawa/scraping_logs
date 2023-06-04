"""
要件

タスク発注するパターンを3つに分ける
ファイルリストを作成する
ファイルリストを使って、タスク発注する

タスク発注は、datetimeを使って現時刻を取得し、タスク発注する時間になったら、
現時刻から指定時間前の時間から現時刻までの間にを発注する

"""

import configparser
import ast
import datetime
import random


# タスク発注する時間になったら、タスク発注する
def task_order(now, hours: int, minutes: int):
    # 現在時刻を取得
    # now = datetime.datetime.now().time()
    # タスク発注可能な時間は, 00:00:00 ~ 00:10:00
    target_time: datetime = datetime.time(hours, minutes, 0) <= now.time() <= datetime.time(hour=hours, minute=minutes+10, second=0)
    if target_time:
        print("The current time is")
        # タスク発注する時間を取得
        return True
    else:
        print("The current time is not")
        return False

def time_tasks(now, tasks: list):
    for hour, min, time_back in tasks:
      if task_order(now, hour, min):
          return int(time_back)
    return False

def get_service_number():
    # サービス番号を取得
    service_number = random.randint(1, 15)
    return service_number

def read_file(file_name: str, section: str, tasks_key: str, service_numbers_key=None) -> tuple:

    config_ini = configparser.ConfigParser()
    config_ini.read(file_name, encoding='utf-8')
    
    tasks_str = config_ini[section][tasks_key]
    tasks = ast.literal_eval(tasks_str)

    # もし service_numbers_key がある場合
    if service_numbers_key is not None:
        service_numbers_str = config_ini[section][service_numbers_key]
        service_numbers = ast.literal_eval(service_numbers_str)
        return tasks, service_numbers
    else:
        return tasks, None

def target_task_time(now: datetime, service_number: int):

    tasks_first, service_numbers_first = read_file('tasks.ini', 'FIRST_TASKS', 'tasks', 'service_numbers')
    tasks_second, service_numbers_second = read_file('tasks.ini', 'SECOND_TASKS', 'tasks', 'service_numbers')
    tasks_default, _ = read_file('tasks.ini', 'DEFAULT', 'tasks', None)

    print({'service_number:', service_number})
    if service_number in service_numbers_first:
        # pattern1
        time_back = time_tasks(now, tasks_first)
        if time_back:
            return time_back + 10
        return 0
    elif service_number in service_numbers_second:
        # pattern2
        time_back = time_tasks(now, tasks_second)
        if time_back:
            return time_back + 10
        return 0
    else:
        # default
        time_back = time_tasks(now, tasks_default)
        if time_back:
            return time_back + 10
        return 0

def result_time(now: datetime) -> tuple[int, int]:
    """発注する時間を取得する"""""
    target_time = target_task_time(now, service_number=get_service_number())
    if target_time == 0:
        return 0, 0
 
    # 発注する時間を取得
    since = datetime.datetime.combine(datetime.date.today(), now.time()) - datetime.timedelta(minutes=target_time)

    # str型に変換
    since = since.strftime('%Y-%m-%dT%H:%M:%S')
    until = now.strftime('%Y-%m-%dT%H:%M:%S')

    return since, until

def main():
    """メイン処理"""
    now = datetime.datetime.now()
    since, until = result_time(now)
    print({'since:': since, 'until:': until})


if __name__ == '__main__':
    main()