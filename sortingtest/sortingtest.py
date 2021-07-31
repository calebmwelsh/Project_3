def addTask():
    schedule = open("testarray","a")
    print("Would you like to add a task?")
    print("1. Yes")
    print("2. No")
    choice=input("Enter your selection number here:")

    if choice=="1":
        print("What type of task is it?")
        print("1. Homework ")
        print("2. Workout")
        print("3. Leisure")
        type=input("Enter your selection number here:")
        name11=input("Title your task:")
    elif choice=="2":
        quit
    else:
        print("Invalid option, please input a number corresponding to the named option.")
        addTask()

    homework = 0
    workout = 30
    leisure = 60

    if type=="1":
        homework = homework + 1
        schedule.write("\n")
        schedule.write("[")
        schedule.write(str(homework))
        schedule.write(",120,")
        schedule.write(name11)
        schedule.write("]")
    elif type=="2":
        homework = workout + 1
        schedule.write("\n")
        schedule.write("[")
        schedule.write(str(workout))
        schedule.write(",30,")
        schedule.write(name11)
        schedule.write("]")
    elif type=="3":
        homework = leisure + 1
        schedule.write("\n")
        schedule.write("[")
        schedule.write(str(leisure))
        schedule.write(",20,")
        schedule.write(name11)
        schedule.write("]")
    else:
        print("Invalid option, please restart and input a number corresponding to the named option.")
        addTask
    schedule.close()
addTask()
