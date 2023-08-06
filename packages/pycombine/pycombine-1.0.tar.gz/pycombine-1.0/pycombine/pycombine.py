import sys


def print_help():
    print("usage: pycombine main_file [file ...]")


def pycombine():
    main_file = None
    file_deb = True

    if len(sys.argv) == 1:
        print_help()
        sys.exit()

    for arg in sys.argv:
        if file_deb:
            file_deb = False
            continue

        try:
            if main_file is None:
                main_file = open(arg, "a")
                continue
            else:
                file = open(arg)
        except FileNotFoundError:
            print(f"pycombine: error: the following argument file {arg} cannot be found.")
            sys.exit()
        else:
            main_file.write("\n" + file.read())
