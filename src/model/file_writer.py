def write(text):
    f = open('../data/log.txt', 'a')
    f.write(str(text))
    f.close()


def read_log():
    f = open('../data/log.txt', 'r')
    return f.read()
