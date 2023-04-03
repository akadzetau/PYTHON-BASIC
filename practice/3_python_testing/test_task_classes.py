"""
Write tests for classes in 2_python_part_2/task_classes.py (Homework, Teacher, Student).
Check if all methods working correctly.
Also check corner-cases, for example if homework number of days is negative.
"""
import io
import importlib
from unittest import TestCase
import datetime
from unittest.mock import patch
res = importlib.import_module('practice.2_python_part_2.task_classes')


class Test_сlasses(TestCase):
    def setUp(self) -> None:
        self.teacher = res.Teacher('Orlyakov', 'Dmitry')
        self.student = res.Student('Popov', 'Vladislav')

        self.expired_homework = self.teacher.create_homework('Learn functions', 0)
        create_homework_too = self.teacher.create_homework
        self.oop_homework = create_homework_too('create 2 simple classes', 5)

    def test_teacher_names(self):
        assert self.teacher.last_name == 'Orlyakov'
        assert self.teacher.first_name == 'Dmitry'

    def test_teacher_home_work0(self):
        assert isinstance(self.expired_homework.created, datetime.datetime), "expired_homework.created is not TS type"
        assert self.expired_homework.deadline == datetime.timedelta(0), "Deadline should be 0"
        assert self.expired_homework.text == 'Learn functions', "Text should be \"Learn functions\""

    def test_teacher_home_work5(self):
        assert isinstance(self.oop_homework.created, datetime.datetime), "expired_homework.created is not TS type"
        assert self.oop_homework.deadline == datetime.timedelta(5), "Deadline should be 5"
        assert self.oop_homework.text == 'create 2 simple classes', "Text should be \"create 2 simple classes\""

    def test_student_names(self):
        assert self.student.last_name == 'Popov'
        assert self.student.first_name == 'Vladislav'

    def test_homework_is_active(self):
        assert not self.expired_homework.is_active(), "Expired homework should not be active"
        assert self.oop_homework.is_active(), "Not expired homework should be active"

    def test_student_hw1(self):
        do_hw = self.student.do_homework(self.oop_homework)
        assert isinstance(do_hw, res.Homework), "Should be Homework class"

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_student_hw_ex(self, mock_stdout):
        self.student.do_homework(self.expired_homework)
        expected_print = 'You are late\n'
        assert expected_print == mock_stdout.getvalue(), "Should print \"You are late\""
