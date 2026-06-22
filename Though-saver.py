import json
import os
from datetime import datetime, timedelta
from collections import Counter

from notion_client import Client
from dotenv import load_dotenv
import os

load_dotenv()

notion = Client(auth=os.getenv("NOTION_TOKEN"))
database_id = os.getenv("NOTION_DATABASE_ID")

notion.pages.create(
    parent={"database_id": database_id},
    properties={
        "Thought": {
            "title": [
                {
                    "text": {
                        "content": "API Test"
                    }
                }
            ]
        }
    }
)

print("Connected to Notion!")

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
    print("\n=== Personal Thought Journal ===\n")
    
    while True:
        thoughts = load_thoughts()
        
        print("\nWhat would you like to do?")
        print("1. Save new thought")
        print("2. View all thoughts")
        print("3. Search thoughts (text)")
        print("4. Search by tags")
        print("5. View statistics")
        print("6. Weekly Summary")
        print("7. Edit entry")
        print("8. Delete entry")
        print("9. Quit")
        
        choice = input("\nChoose (1-9): ").strip()

        if choice == "1":
            save_new_thought(thoughts)
        elif choice == "2":
            view_thoughts(thoughts)
        elif choice == "3":
            search_thoughts(thoughts)
        elif choice == "4":
            search_by_tags(thoughts)
        elif choice == "5":
            show_statistics(thoughts)
        elif choice == "6":
            weekly_summary(thoughts)
        elif choice == "7":
            edit_thought(thoughts)
        elif choice == "8":
            delete_thought(thoughts)
        elif choice in ["9", "q", "quit"]:
            print("👋 Goodbye! Your thoughts are saved.")
            break
        else:
            print("Invalid choice. Please try again.")

def save_new_thought(thoughts):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    thought_text = input("Enter thought: ").strip()
    while True:
        try:
            mood_score = int(input("Mood (1-10): "))
            if 1 <= mood_score <= 10:
                break
            print("Please enter a number between 1 and 10.")
        except:
            print("Please enter a valid number.")

    feeling = input("How are you feeling? ").strip()
    tags = input("Tags (comma separated, optional): ").strip()
    tag_list = [t.strip().lower() for t in tags.split(",")] if tags else []

    new_entry = {
        "timestamp": timestamp,
        "thought": thought_text,
        "mood": mood_score,
        "feeling": feeling,
        "tags": tag_list
    }

    thoughts.append(new_entry)
    save_thoughts(thoughts)
    print("✅ Thought saved successfully!")

def show_list(thoughts):
    """Helper to show numbered list"""
    if not thoughts:
        print("No thoughts yet.")
        return False
    for i, entry in enumerate(thoughts):
        tags_str = ", ".join(entry.get('tags', [])) if entry.get('tags') else "No tags"
        print(f"{i+1}. [{entry['timestamp'][:10]}] {entry['thought'][:50]}... | Tags: {tags_str}")
    return True

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

def search_by_tags(thoughts):
    if not thoughts:
        print("No thoughts yet.")
        return
    tag_search = input("Enter tag(s) to search (comma separated): ").strip().lower()
    if not tag_search:
        return
    search_tags = [t.strip() for t in tag_search.split(",")]
    found = False
    print(f"\nResults for tags: {search_tags}")
    for entry in thoughts:
        entry_tags = entry.get('tags', [])
        if any(st in entry_tags for st in search_tags):
            print("\n" + "="*60)
            print(f"[{entry['timestamp']}]")
            print(f"Thought: {entry['thought']}")
            print(f"Mood: {entry['mood']}/10")
            print(f"Feeling: {entry['feeling']}")
            print(f"Tags: {', '.join(entry_tags)}")
            found = True
    if not found:
        print("No entries found with those tags.")

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
                entry['tags'] = [t.strip().lower() for t in tags.split(",")]
            
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

def show_statistics(thoughts):
    if not thoughts:
        print("No thoughts yet.")
        return
    moods = [entry['mood'] for entry in thoughts]
    print(f"\nTotal thoughts: {len(thoughts)}")
    print(f"Average mood: {sum(moods)/len(moods):.1f}/10")

def weekly_summary(thoughts):
    if not thoughts:
        print("No thoughts yet.")
        return

    today = datetime.now()
    week_ago = today - timedelta(days=7)
    
    recent = [e for e in thoughts if datetime.strptime(e['timestamp'], "%Y-%m-%d %H:%M:%S") >= week_ago]
    
    if not recent:
        print("No entries in the last 7 days.")
        return

    print("\n" + "="*60)
    print("📅 Weekly Summary (Last 7 Days)")
    print("="*60)
    
    moods = [e['mood'] for e in recent]
    avg_mood = sum(moods) / len(moods)
    
    all_tags = []
    for e in recent:
        all_tags.extend(e.get('tags', []))
    common_tags = Counter(all_tags).most_common(5)
    
    print(f"Total entries this week: {len(recent)}")
    print(f"Average mood: {avg_mood:.1f}/10")
    print(f"Highest mood: {max(moods)} | Lowest mood: {min(moods)}")
    
    if common_tags:
        print("\nMost used tags:")
        for tag, count in common_tags:
            print(f"  • {tag} ({count} times)")
    
    print("\nKeep going! Consistency is powerful.")

if __name__ == "__main__":
    main()
