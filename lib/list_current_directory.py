import os


def list_files():
    file_types = {}
    file_types["folder"] = []
    files = os.listdir('.')
    for f in files:
        if os.path.isfile(f):
            try:
                pos_dot = str(f).index('.')
                ext = str(f)[pos_dot:]
            except ValueError:
                ext = "Not extension"
            if ext in file_types:
                file_types[ext] += 1
            else:
                file_types[ext] = 1
        else:
            file_types["folder"].append(f)
    return file_types

def check_sub_directory():
    directorys = list_files()
    for file in directorys["folder"]:
        sub_files = os.listdir(file)
        sub_path = os.path.realpath(file)
        for sub_file in sub_files:
            sub_file = sub_path + "\\" + sub_file
            if os.path.isfile(sub_file):
                print sub_file

def test_function():
    for root, dirs, files in os.walk("..", topdown=False):
        for name in files:
            print(os.path.join(root, name))
        # for name in dirs:
        #     print(os.path.join(root, name))

def test_function2():
    for root, dirs, files in os.walk("."):
        for file in files:
            if file == "main.py":
                print(os.path.join(root, file))
