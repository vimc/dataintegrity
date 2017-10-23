
def sql_equal(a, b):
    return a == b or ((a != a) and (b != b))


def array_equal(x, y):
    for i in range(0, len(x)):
        if not sql_equal(x[i], y[i]):
            print("Not equal: {old}, {new}".format(old=x[i], new=y[i]))
            return False
    return True