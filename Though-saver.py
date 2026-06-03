from datetime import datetime

choice = input("1. Save thought\n2. View thoughts\n3. Search thoughts\nChoose: ")

if choice == "1":
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    thought = input("Enter thought: ")
    with open("thoughts.txt", "a") as file:
        file.write("-" * 40 + "\n")
        file.write(timestamp + "\n")
        file.write(thought + "\n\n")
    print(thought)
elif choice == "2":
    try:
        with open("thoughts.txt", "r") as file:
            print(file.read())
    except FileNotFoundError:
        print("No thoughts saved yet.")

elif choice == "3":
    search_term = input("Enter search term: ").lower()

    try:
        with open("thoughts.txt", "r") as file:
            thoughts = file.read()

        entries = [e for e in thoughts.split("-" * 40) if e.strip()]


        found = False

        for entry in entries:
            if search_term in entry.lower():
                print("-" * 40)
                print(entry.strip())
                found = True

        if not found:
            print("No thoughts found containing the search term.")

    except FileNotFoundError:
        print("No thoughts saved yet.")