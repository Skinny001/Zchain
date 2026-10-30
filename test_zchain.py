import sys
import subprocess
import pytest

def run_zchain(args):
    result = subprocess.run(
        [sys.executable, "zchain.py"] + args,
        capture_output=True,
        text=True
    )
    return result

def test_invalid_command():
    res = run_zchain(["invalidcommand"])
    assert res.returncode != 0
    assert "Error" in res.stderr

def test_missing_command():
    res = run_zchain([])
    assert res.returncode != 0
    assert "Error" in res.stderr