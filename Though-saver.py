import json
import os
from datetime import datetime, timedelta
from collections import Counter

from notion_client import Client
from dotenv import load_dotenv

# ====================== NOTION SETUP ======================
load_dotenv()

notion = Client(auth=os.getenv("NOTION_TOKEN"))
database_id = os.getenv("NOTION_DATABASE_ID")

FILE_NAME = "thoughts.json"

# ====================== LOCAL STORAGE FUNCTIONS ======================
def load_thoughts():
    """Load thoughts from local JSON file"""
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r", encoding="utf-8") as file:
                return json.load(file)
        except:
            return []
    return []


def save_thoughts(thoughts):
    """Save thoughts to local JSON file"""
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(thoughts, file, indent=2, ensure_ascii=False)


# ====================== NOTION INTEGRATION ======================
def create_notion_page(entry):
    """
    Creates a rich page in Notion database with:
    - Custom page title
    - Mood (number)
    - Tags (multi-select)
    - Full thought content inside the page
    """
    try:
        # Use custom title or generate from thought
        title = entry.get("title") or entry["thought"][:60] + ("..." if len(entry["thought"]) > 60 else "")

        properties = {
            # === CHANGE THESE KEYS IF YOUR DATABASE PROPERTY NAMES ARE DIFFERENT ===
            "Name": {  # This should be your Title property
                "title": [
                    {
                        "text": {
                            "content": title
                        }
                    }
                ]
            },
            "Mood": {
                "number": entry["mood"]
            },
            "Tags": {
                "multi_select": [{"name": tag} for tag in entry.get("tags", [])]
            },
            "Date": {  # Optional but recommended
                "date": {
                    "start": datetime.strptime(entry["timestamp"], "%Y-%m-%d %H:%M:%S").isoformat()
                }
            }
        }

        # Create page with content blocks
        page = notion.pages.create(
            parent={"database_id": database_id},
            properties=properties,
            children=[
                # Main thought content
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": entry["thought"]
                                }
                            }
                        ]
                    }
                },
                # Feeling as second paragraph
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": f"Feeling: {entry.get('feeling', 'Not specified')}"
                                }
                            }
                        ]
                    }
                }
            ]
        )
        print(f"✅ Successfully created in Notion: \"{title}\"")
        return page

    except Exception as e:
        print(f"❌ Failed to create Notion page: {e}")
        print("   → Make sure your database has these properties:")
        print("     • Name (Title type)")
        print("     • Mood (Number type)")
        print("     • Tags (Multi-select type)")
        print("     • Date (Date type - optional)")
        return None


# ====================== MAIN FEATURES ======================
def save_new_thought(thoughts):
    """Save a new thought both locally and to Notion"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print("\n--- New Thought Entry ---")
    title = input("Page title (optional, press Enter to auto-generate): ").strip()
    
    thought_text = input("Enter your thought: ").strip()
    
    # Mood input with validation
    while True:
        try:
            mood_score = int(input("Mood (1-10): "))
            if 1 <= mood_score <= 10:
                break
            print("Please enter a number between 1 and 10.")
        except:
            print("Please enter a valid number.")

    feeling = input("How are you feeling? ").strip()
    tags_input = input("Tags (comma separated, optional): ").strip()
    tag_list = [t.strip().lower() for t in tags_input.split(",") if t.strip()]

    # Create entry for local storage
    new_entry = {
        "timestamp": timestamp,
        "title": title or (thought_text[:60] + ("..." if len(thought_text) > 60 else "")),
        "thought": thought_text,
        "mood": mood_score,
        "feeling": feeling,
        "tags": tag_list
    }

    # Save locally
    thoughts.append(new_entry)
    save_thoughts(thoughts)
    print("✅ Thought saved locally!")

    # Sync to Notion
    create_notion_page(new_entry)


def show_list(thoughts):
    """Helper to show numbered list of thoughts"""
    if not thoughts:
        print("No thoughts yet.")
        return False
    for i, entry in enumerate(thoughts):
        tags_str = ", ".join(entry.get('tags', [])) if entry.get('tags') else "No tags"
        print(f"{i+1}. [{entry['timestamp'][:10]}] {entry['thought'][:50]}... | Tags: {tags_str}")
    return True


def view_thoughts(thoughts):
    """View all thoughts in detail"""
    if not thoughts:
        print("No thoughts saved yet.")
        return
    for entry in thoughts:
        print("\n" + "="*70)
        print(f"📅 {entry['timestamp']}")
        print(f"📌 Title: {entry.get('title', 'No title')}")
        print(f"💭 Thought: {entry['thought']}")
        print(f"😊 Mood: {entry['mood']}/10")
        print(f"❤️ Feeling: {entry['feeling']}")
        if entry.get('tags'):
            print(f"🏷️  Tags: {', '.join(entry['tags'])}")


# ====================== OTHER FUNCTIONS (unchanged logic) ======================
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
            
            entry['title'] = input(f"Title [{entry.get('title', '')}]: ").strip() or entry.get('title')
            entry['thought'] = input(f"Thought [{entry['thought'][:50]}...]: ").strip() or entry['thought']
            entry['feeling'] = input(f"Feeling [{entry['feeling']}]: ").strip() or entry['feeling']
            
            new_mood = input(f"Mood (1-10) [{entry['mood']}]: ").strip()
            if new_mood:
                try:
                    entry['mood'] = int(new_mood)
                except:
                    print("Invalid mood, keeping old value.")
            
            tags = input(f"Tags [{', '.join(entry.get('tags', []))}]: ").strip()
            if tags:
                entry['tags'] = [t.strip().lower() for t in tags.split(",") if t.strip()]
            
            save_thoughts(thoughts)
            print("✅ Entry updated locally!")
            # Optional: update Notion page too (advanced feature)
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


# ====================== MAIN MENU ======================
def main():
    print("\n=== Personal Thought Journal with Notion ===\n")
    print("Notion integration is active ✅\n")
    
    while True:
        thoughts = load_thoughts()
        
        print("\nWhat would you like to do?")
        print("1. Save new thought (Local + Notion)")
        print("2. View all thoughts (local)")
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


if __name__ == "__main__":
    main()
