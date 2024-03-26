def Input(message, choices, end=None):
    print(message)
    for i in range(len(choices)):
        print(str(i + 1) + " : " + str(choices[i]))
    if end is not None:
        print(end)
    while True is True:
        ans = input(">> ")
        for i in range(len(choices)):
            if str(i + 1) in ans:
                return int(i)
        print("I didn't quite catch your request.")
        print("Simply type '1' for the first choice, '2' for the second, etc.")
