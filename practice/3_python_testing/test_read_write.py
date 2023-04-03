"""
Write tests for 2_python_part_2/task_read_write.py task.
To write files during tests use temporary files:
https://docs.python.org/3/library/tempfile.html
https://docs.pytest.org/en/6.2.x/tmpdir.html
"""
import importlib
res = importlib.import_module('practice.2_python_part_2.task_read_write')

CONTENT = ["1","2","3"]
RESULT_FILE = "result.txt"

def test_read_write(tmp_path):
    d = tmp_path / "dr"
    d.mkdir()

    # Create test files
    for i in CONTENT:
        p = d / f"file_{i}.txt"
        p.write_text(i)

    # Read test files
    content = res.read_files(d)
    pr = d / RESULT_FILE
    # Write result file
    res.write_file(pr, content)

    assert pr.read_text() == ", ".join(CONTENT)