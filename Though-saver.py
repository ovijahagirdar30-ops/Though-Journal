from datetime import datetime
import json
import os

FILE_NAME = "thoughts.json"

def load_thoughts():
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r", encoding="utf-8") as file:
                return json.load(file)
        except:
            return []
    return []

def save_thoughts(thoughts):
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(thoughts, file, indent=2, ensure_ascii=False)

def main():
    print("\n=== Personal Thought Journal (JSON Version) ===\n")
    thoughts = load_thoughts()

    choice = input("1. Save thought\n2. View all thoughts\n3. Search thoughts\n4. View statistics\nChoose (1-4): ").strip()

    if choice == "1":
        save_new_thought(thoughts)
    elif choice == "2":
        view_thoughts(thoughts)
    elif choice == "3":
        search_thoughts(thoughts)
    elif choice == "4":
        show_statistics(thoughts)
    else:
        print("Invalid choice.")

def save_new_thought(thoughts):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    thought_text = input("Enter thought: ").strip()
    while True:
        try:
            mood_score = int(input("Mood (1-10): "))
            if 1 <= mood_score <= 10:
                break
            print("Please enter a number between 1 and 10.")
        except ValueError:
            print("Please enter a valid number.")

    feeling = input("How are you feeling? ").strip()
    tags = input("Tags (comma separated, optional): ").strip()
    tag_list = [t.strip() for t in tags.split(",")] if tags else []

    new_entry = {
        "timestamp": timestamp,
        "thought": thought_text,
        "mood": mood_score,
        "feeling": feeling,
        "tags": tag_list
    }

    thoughts.append(new_entry)
    save_thoughts(thoughts)
    print(f"✅ Thought saved successfully! Mood: {mood_score}/10")

def view_thoughts(thoughts):
    if not thoughts:
        print("No thoughts saved yet.")
        return
    for entry in thoughts:
        print("\n" + "="*60)
        print(f"[{entry['timestamp']}]")
        print(f"Thought: {entry['thought']}")
        print(f"Mood: {entry['mood']}/10")
        print(f"Feeling: {entry['feeling']}")
        if entry['tags']:
            print(f"Tags: {', '.join(entry['tags'])}")

def search_thoughts(thoughts):
    term = input("Enter search term: ").lower().strip()
    found = False
    for entry in thoughts:
        if (term in entry['thought'].lower() or 
            term in entry['feeling'].lower() or
            any(term in tag.lower() for tag in entry['tags'])):
            print("\n" + "="*60)
            print(f"[{entry['timestamp']}]")
            print(f"Thought: {entry['thought']}")
            print(f"Mood: {entry['mood']}/10")
            found = True
    if not found:
        print("No matching thoughts found.")

def show_statistics(thoughts):
    if not thoughts:
        print("No thoughts yet.")
        return
    moods = [entry['mood'] for entry in thoughts]
    print(f"\nTotal thoughts: {len(thoughts)}")
    print(f"Average mood: {sum(moods)/len(moods):.1f}/10")

if __name__ == "__main__":
    main()
