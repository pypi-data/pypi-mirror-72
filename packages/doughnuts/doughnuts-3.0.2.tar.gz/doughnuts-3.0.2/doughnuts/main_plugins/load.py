from libs.config import alias, color, gset, gget
from os import path, SEEK_SET


@alias(True, "l")
def run(id: int = 0):
    """
    load

    Load a webshell from log.

    eg: load {_id}
    """
    pf = gget("main.pf")
    if (not path.exists("webshell.log")):
        print(color.red("No webshell.log"))
        return
    f = open("webshell.log", "r+")
    lines = f.readlines()
    f.seek(0, SEEK_SET)
    try:
        if (id <= 0):
            line_num = pf["show"].run()
            load_id = input("choose:>")
            # load_id = int(load_id) if load_id.isdigit() else 1
            if (load_id.isdigit()):
                load_id = int(load_id)
            else:
                print(color.red("\nInput Error\n"))
                return
        else:
            load_id = id
            line_num = len(lines)
        if load_id <= line_num:
            data = lines[load_id - 1].strip().split("|")
            gset("webshell.from_log", True, namespace="webshell")
            connect = pf["connect"].run(*data)
            if (not connect):
                print("This webshell seems to no longer working, do you want to delete it?")
                flag = input("(YES/no) >")
                if (flag.lower() in ['n', 'no']):
                    return
                del lines[load_id - 1]
                print("".join(lines))
                f.write("".join(lines))
        else:
            print(color.red("ID error"))
    finally:
        f.close()
