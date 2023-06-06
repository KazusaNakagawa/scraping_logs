import ast
import yaml
import pathlib

# task.ymlのパスを取得: pathlibをつかって
task_path = pathlib.Path(__file__).parent / 'config' / 'task.yml'

# task.ymlを読み込む
with open(task_path, 'r', encoding='utf-8') as f:
    task = yaml.safe_load(f)

# print(task['time_interval'])

"""
{
  "default": {
    "interval": ["(0, 0)", "(4, 0)", "(8, 0)"],
    "service_numbers": ["b000", "b001", "b002"]
  },
  "pattern1": {
    "interval": ["(0, 0)"],
    "service_numbers": ["b004", "b001", "b002"]
  },
  "pattern2": {
    "interval": ["(0, 0)", "(10, 0)"],
    "service_numbers": ["b005", "b006", "b007"]
  }
}
"""
# 以上のjson を共通メソッドを作成し、今後　task.ymlの中身を変更しても、共通メソッドを改修しなくてもよい関数を作成する


def process_patterns(patterns):
    """
    {
        "default": {
            "interval": [(0, 0), (4, 0), (8, 0)],
            "service_numbers": None
        },
        "pattern1": {
            "interval": [(0, 0)],
            "service_numbers": ["b008", "b009", "b010"]
        },
        "pattern2": {
            "interval": [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (9, 0), (10, 0), (11, 0), (12, 0), (13, 0), (14, 0), (15, 0), (16, 0), (17, 0), (18, 0), (19, 0), (20, 0), (21, 0), (22, 0), (23, 0)],
            "service_numbers": ["b005", "b006", "b007"]
        }
    }
    """

    settings = {}

    for pattern_name, pattern_data in patterns.items():
        intervals = pattern_data.get('interval')
        if intervals:
            interval_tuple = [ast.literal_eval(intarval) for intarval in intervals]
        service_numbers = pattern_data.get('service_numbers')

        # コメント に記載のある json 形式で settings に追加
        settings[pattern_name] = {
            'interval': interval_tuple,
            'service_numbers': service_numbers
        }

    return settings

r = process_patterns(task['time_interval'])
service_numbers = ['b002', 'b003', 'b005', 'b008']

def target_service_interval(service_numbers, settings):
    sections = [section for section in settings.keys()]
    for service in service_numbers:
        found = False
        for section in sections:
            if settings[section]['service_numbers'] is not None and service in settings[section]['service_numbers']:
                print(f"Service: {service}, Interval: {settings[section]['interval']}")
                found = True
                break
        if not found:
            print(f"Service: {service}, Interval: {settings['default']['interval']}")

target_service_interval(service_numbers, r)