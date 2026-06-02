from datetime import datetime

choice = input("1. Save thought\n2. View thoughts\nChoose: ")

if choice == "1":
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    thought = input("Enter thought: ")
    with open("thoughts.txt", "a") as file:
        file.write("-" * 40 + "\n")
        file.write(timestamp + "\n")
        file.write(thought + "\n\n")
    print(thought)
elif choice == "2":
    with open("thoughts.txt", "r") as file:
        print(file.read())