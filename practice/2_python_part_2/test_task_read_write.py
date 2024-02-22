from unittest import TestCase
from unittest.mock import patch, mock_open
from task_read_write import read_files, write_file


class Test(TestCase):
    def test_read(self):
        path = "files"
        open_mock = mock_open()
        with patch("task_read_write.open", open_mock, create=True):
            read_files(path)

        self.assertEqual(open_mock.call_count, 20)

    def test_write(self):
        open_mock = mock_open()
        with patch("task_read_write.open", open_mock, create=True):
            write_file("output.txt", "1, 2, 3")

        open_mock.assert_called_with("output.txt", "w")
        open_mock.return_value.write.assert_called_once_with("1, 2, 3")