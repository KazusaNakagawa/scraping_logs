from datetime import datetime
import unittest
import src.time_travel as task_time

class TestTask(unittest.TestCase):

    def test_time_intervals(self):
        """Test _get_time_interval function"""
        tasks = [0.0, 4.5, 10.0, 15.5, 23.5]
        mocks_now = [
            datetime(2021, 4, 19, 0, 8, 0),
            datetime(2021, 4, 19, 4, 36, 0),
            datetime(2021, 4, 19, 10, 6, 59),
            datetime(2021, 4, 19, 15, 39, 0),
            datetime(2021, 4, 19, 23, 37, 0),
            ]
        test_time_intervals = [30, 270, 330, 330, 480]
        time_intervals = [task_time._get_time_interval(mock_now, tasks) for mock_now in mocks_now]

        self.assertEqual(time_intervals, test_time_intervals, "time_intervals is not equal to test_time_intervals")

if __name__ == '__main__':
    unittest.main()
