import json
import os
from datetime import datetime

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

def show_list(thoughts):
    """Helper function to show numbered list"""
    if not thoughts:
        print("No thoughts yet.")
        return False
    for i, entry in enumerate(thoughts):
        print(f"{i+1}. [{entry['timestamp'][:10]}] {entry['thought'][:60]}...")
    return True

def main():
    print("\n=== Personal Thought Journal ===\n")
    
    while True:                          # ← New: Persistent loop
        thoughts = load_thoughts()
        
        print("\nWhat would you like to do?")
        print("1. Save new thought")
        print("2. View all thoughts")
        print("3. Search thoughts")
        print("4. View statistics")
        print("5. Edit entry")
        print("6. Delete entry")
        print("7. Quit")
        
        choice = input("\nChoose (1-7): ").strip()

        if choice == "1":
            save_new_thought(thoughts)
        elif choice == "2":
            view_thoughts(thoughts)
        elif choice == "3":
            search_thoughts(thoughts)
        elif choice == "4":
            show_statistics(thoughts)
        elif choice == "5":
            edit_thought(thoughts)
        elif choice == "6":
            delete_thought(thoughts)
        elif choice in ["7", "q", "quit"]:
            print("👋 Goodbye! Your thoughts have been saved.")
            break
        else:
            print("Invalid choice. Please try again.")

# ==================== Rest of the functions (same as before) ====================

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
    print(f"✅ Thought saved successfully!")

def edit_thought(thoughts):
    if not show_list(thoughts):
        return
    try:
        index = int(input("\nEnter number of entry to edit: ")) - 1
        if 0 <= index < len(thoughts):
            entry = thoughts[index]
            print("\nEditing entry...")
            
            entry['thought'] = input(f"Thought [{entry['thought']}]: ").strip() or entry['thought']
            entry['feeling'] = input(f"Feeling [{entry['feeling']}]: ").strip() or entry['feeling']
            
            new_mood = input(f"Mood (1-10) [{entry['mood']}]: ").strip()
            if new_mood:
                try:
                    entry['mood'] = int(new_mood)
                except:
                    print("Invalid mood, keeping old value.")
            
            tags = input(f"Tags [{', '.join(entry.get('tags', []))}]: ").strip()
            if tags:
                entry['tags'] = [t.strip() for t in tags.split(",")]
            
            save_thoughts(thoughts)
            print("✅ Entry updated successfully!")
        else:
            print("Invalid number.")
    except:
        print("Invalid input.")

def delete_thought(thoughts):
    if not show_list(thoughts):
        return
    try:
        index = int(input("\nEnter number of entry to delete: ")) - 1
        if 0 <= index < len(thoughts):
            confirm = input(f"Delete this entry? (y/n): ").lower()
            if confirm == 'y':
                deleted = thoughts.pop(index)
                save_thoughts(thoughts)
                print(f"✅ Entry deleted!")
            else:
                print("Delete cancelled.")
        else:
            print("Invalid number.")
    except:
        print("Invalid input.")

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
        if entry.get('tags'):
            print(f"Tags: {', '.join(entry['tags'])}")

def search_thoughts(thoughts):
    term = input("Enter search term: ").lower().strip()
    found = False
    for entry in thoughts:
        if (term in entry['thought'].lower() or 
            term in entry['feeling'].lower() or
            any(term in tag.lower() for tag in entry.get('tags', []))):
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
