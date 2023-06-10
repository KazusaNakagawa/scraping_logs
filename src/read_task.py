import yaml
import pathlib

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

def main():
    task = read_file(task_path)
    r = process_patterns(task['time_interval'])
    service_numbers = ['b001', 'b005', 'b008']
    for service_number in service_numbers:
        print(target_service_interval(service_number, r))


if __name__ == '__main__':
    main()
