from datetime import datetime

choice = input("1. Save thought\n2. View thoughts\n3. Search thoughts\nChoose: ")

if choice == "1":
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    thought = input("Enter thought: ")

    while True:
        try:
            mood_score = int(input("Mood (1-10): "))
            if 1 <= mood_score <= 10:
                break
            print("Please enter a number between 1 and 10.")
        except ValueError:
            print("Please enter a valid number.")

    mood_note = input("How are you feeling? ")

    with open("thoughts.txt", "a") as file:
        file.write("-" * 40 + "\n")
        file.write(f"[{timestamp}]\n")
        file.write(f"Thought: {thought}\n")
        file.write(f"Mood: {mood_score}/10\n")
        file.write(f"Feeling: {mood_note}\n\n")

    print(f"Saved! Mood logged as {mood_score}/10.")

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