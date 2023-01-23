def adb_port(number):
    # path to bluestacks logs
    filename = fr"D:\Bluestacks Engines\BlueStacks_nxt\bluestacks.conf"

    with open(filename, 'r') as f:
        search = 'Nougat64'
        if int(number) != 1:
            search += f"_{int(number)}"

        for line in f:
            if line[:3] != "bst":
                continue

            words = line.split('.')
            if len(words) < 5:
                continue

            if words[2] != search:
                continue

            if words[3] != 'status':
                continue

            if words[4][:8] != 'adb_port':
                continue

            adb_port = words[4].split('"')[1]
            return adb_port
