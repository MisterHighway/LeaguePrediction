def write(text):
    f = open('../Data/log.txt', 'a')
    f.write(str(text))
    f.close()


def read_log():
    f = open('../Data/log.txt', 'r')
    return f.read()
