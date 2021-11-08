def write(text):
    f = open('../Data/log_2.txt', 'a')
    f.write(str(text))
    f.close()


def read_log():
    f = open('../Data/log_2.txt', 'r')
    return f.read()
