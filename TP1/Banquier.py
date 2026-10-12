def func():
    val=2.71828
    for i in range(1,50):
        val= val - 1.0
        val*=i
        print(val)
    print(val)
    return val

func()