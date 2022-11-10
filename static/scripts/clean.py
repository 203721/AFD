from os import remove, listdir


def clean():
    path = ""
    files = "files/"
    dir = listdir(files)
    if dir:
        for file in dir:
            path = files + file
            remove(path)


def main():
    clean()


if __name__ == "__main__":
    main()
