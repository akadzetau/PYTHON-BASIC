"""
Write tests for 2_python_part_2/task_read_write_2.py task.
To write files during tests use temporary files:
https://docs.python.org/3/library/tempfile.html
https://docs.pytest.org/en/6.2.x/tmpdir.html
"""
import importlib

res = importlib.import_module('practice.2_python_part_2.task_read_write_2')
RND_WORDS = ['abc', 'def', 'xyz']
RESULT_FILE1 = "result1.txt"
RESULT_FILE2 = "result2.txt"


def test_read_write_file1(tmp_path):
    d = tmp_path / "dr"
    d.mkdir()

    pr = d / RESULT_FILE1
    # Write result file
    res.write_n(pr, RND_WORDS)

    assert pr.read_text("UTF-8") == "abc\ndef\nxyz"


def test_read_write_file2(tmp_path):
    d = tmp_path / "dr"
    d.mkdir()

    pr = d / RESULT_FILE2
    # Write result file
    res.write_rev_sep(pr, RND_WORDS)

    assert pr.read_text("CP1252") == "xyz,def,abc"
