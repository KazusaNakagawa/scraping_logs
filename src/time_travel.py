import datetime
import pathlib
import yaml

# task.ymlのパスを取得: pathlibをつかって
# config は、src と同じ階層にあるとする
task_path = pathlib.Path(__file__).parent.cwd() / 'config' / 'task.yml'

def read_file(read_file) -> dict:
    """yaml ファイルを読み込んで、dict に変換して返す

    Args:
        read_file (str): 読み込むファイルのパス

    Returns:
        dict: yaml ファイルの中身
    """
    with open(read_file, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def process_patterns(patterns) -> dict:
    """patterns を処理して、settings を返す

    Args:
        patterns (dict): patterns の中身

    Returns:
        dict: settings の中身
    """
    settings = {}

    for pattern_name, pattern_data in patterns.items():
        intervals = pattern_data.get('interval')
        service_numbers = pattern_data.get('service_numbers')

        # コメント に記載のある json 形式で settings に追加
        settings[pattern_name] = {
            'interval': intervals,
            'service_numbers': service_numbers
        }

    return settings

def target_service_interval(service_number, settings):
    """service_number に対応する interval を返す

    Args:
        service_number (str): サービス番号
        settings (dict): settings の中身

    Returns:
        dict: interval の中身
    """

    sections = [section for section in settings]
    task_section = 'default'

    for section in sections:
        if settings[section]['service_numbers'] is not None\
            and service_number in settings[section]['service_numbers']:
            task_section = section
            break
    return {
        'service_number': service_number,
        'section': task_section,
        'interval': settings[task_section]['interval']
        }

def _get_time_interval(now, tasks) -> int:
    """タスク発注する時間を取得する

    Args:
        now (datetime): 現在時刻
        tasks (list): タスク発注する時間のリスト

    Returns:
        [int]: タスク発注する時間を取得する

    """
    # Define the mocked time interval
    time_interval: int = 0

    hour, minute = now.strftime("%H,%M").split(",")
    minute = int(int(minute) / 10) * 10
    # tasks に格納されている値に, 10分単位で丸める.
    # 意図は、実行時間を10分単位で丸めることで、実行時間の猶予を9min作る.
    task_time = int(hour) + minute / 60

    if not task_time in tasks:
        return time_interval

    """NOTE: コード理解のため.分割して書いた """
    # taeget task index
    task_index = tasks.index(task_time)
    # before task time diffrence
    before_time_diff = tasks[task_index] - tasks[(task_index -1)%len(tasks)]
    # convert to hours
    _ = int(before_time_diff%24 * 60)

    # one line
    time_interval = int(((tasks[tasks.index(task_time)] - tasks[(tasks.index(task_time) -1)%len(tasks)])%24) *60)

    return time_interval

def get_task_time_interval(now: datetime, time_interval) -> tuple:
    """タスク発注する時間を取得する

    Args:
        now (datetime): 現在時刻
        time_interval (int): タスク発注する時間のリスト

    Returns:
        [int]: タスク発注する時間を取得する. 時間外の場合は、None を返す.

    """

    if time_interval == 0:
        return None, None

    since = datetime.datetime.combine(datetime.date.today(), now.time()) - datetime.timedelta(minutes=time_interval)

    # str型に変換
    since = since.strftime('%Y-%m-%dT%H:%M:%S')
    until = now.strftime('%Y-%m-%dT%H:%M:%S')

    return since, until

def main():
    """main function"""
    # now = datetime.now()
    mock_now = datetime.datetime(2021, 4, 19, 0, 8, 0)
    task = read_file(task_path)
    settings = process_patterns(task['time_interval'])
    service_numbers = ['b001', 'b005', 'b008']

    for service_number in service_numbers:
        setting = target_service_interval(service_number, settings)
        time_interval = _get_time_interval(mock_now, setting['interval'])
        since, until = get_task_time_interval(mock_now, time_interval)

        print(f'service_number: {service_number}, section: {setting["section"]}, since: {since}, until: {until}')


if __name__ == '__main__':
    main()
