from functions.get_file_content import get_file_content

wd = "calculator"
tests = ["main.py", "pkg/calculator.py", "/bin/cat", "pkg/does_not_exist.py"]

for t in tests:
    print(get_file_content(wd, t))

#contents = get_file_content("calculator", "lorem.txt")
#print(f'Length: {len(contents)}\nMessage: {contents[10000:]}')

