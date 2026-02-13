from functions.run_python_file import run_python_file

wd = "calculator"

print(run_python_file(wd, "main.py"))
print(run_python_file(wd, "main.py", ["3 + 5"]))
print(run_python_file(wd, "tests.py"))
print(run_python_file(wd, "../main.py"))
print(run_python_file(wd, "nonexistent.py"))
print(run_python_file(wd, "lorem.txt"))
