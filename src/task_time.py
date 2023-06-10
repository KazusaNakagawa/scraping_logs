
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
