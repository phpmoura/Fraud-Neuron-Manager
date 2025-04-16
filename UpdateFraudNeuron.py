# fraud_framework_updater.py
"""
Interactive CLI helper to maintain the Fraud Tactics‑Techniques‑Procedures (TTP) JSON framework stored in **fraudneuron.json**.

Features
========
* Auto‑loads or creates `fraudneuron.json` in the current directory.
* Browse, **add**, or **delete** any Tactic, Technique, or Procedure.
* Parent‑ID validation with on‑the‑fly creation.
* Always prompts for **ID, title, and description** when adding.

Hierarchy
---------
```
root ("tactics")
 └─ Tactic     id → "T*"
     └─ Technique id → "TQ*" (can nest)
         └─ Procedure id → "P*"
```
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict, Optional

########################
# Utility helpers      #
########################

def load_framework(path: Path) -> Dict[str, Any]:
    if path.exists():
        try:
            with path.open("r", encoding="utf‑8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError) as exc:
            print(f"❌  Failed to read {path}: {exc}. Creating fresh skeleton…")
    return {
        "tactics": {
            "id": "T0000",
            "title": "tactics",
            "description": "Methods and techniques used to execute fraudulent operations",
            "items": []
        }
    }


def save_framework(data: Dict[str, Any], path: Path) -> None:
    with path.open("w", encoding="utf‑8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"\n✅  Saved framework to {path.resolve()}")


def find_node_by_id(node: Dict[str, Any], target_id: str) -> Optional[Dict[str, Any]]:
    if node.get("id") == target_id:
        return node
    for child in node.get("items", []):
        result = find_node_by_id(child, target_id)
        if result:
            return result
    return None


def remove_node(node: Dict[str, Any], target_id: str) -> bool:
    """Recursively remove the child whose id==target_id. Returns True if removed."""
    items = node.get("items", [])
    for idx, child in enumerate(items):
        if child.get("id") == target_id:
            del items[idx]
            return True
        if remove_node(child, target_id):
            return True
    return False


def print_tree(node: Dict[str, Any], indent: int = 0) -> None:
    prefix = "  " * indent + ("├─ " if indent else "")
    print(f"{prefix}{node.get('id')} — {node.get('title')}")
    for child in node.get("items", []):
        print_tree(child, indent + 1)


def prompt_entry(id_hint: Optional[str] = None) -> Dict[str, str]:
    new_id = id_hint or input("  > New ID: ").strip()
    if id_hint:
        print(f"  > Using ID: {new_id}")
    title = input("  > Title: ").strip()
    description = input("  > Description: ").strip()
    return {"id": new_id, "title": title, "description": description, "items": []}

########################
# Add / Delete actions #
########################

def add_entry(root: Dict[str, Any]) -> None:
    print("\nCurrent hierarchy:\n")
    print_tree(root["tactics"])
    parent_id = input("\nParent ID (or 'root' for top‑level): ").strip()

    # resolve parent
    if parent_id.lower() == "root":
        parent_node = root["tactics"]
    else:
        parent_node = find_node_by_id(root["tactics"], parent_id)
        if not parent_node:
            if input(f"ID '{parent_id}' not found. Create it? (y/n): ").lower() == "y":
                print(f"\nEnter details for new parent '{parent_id}':")
                parent_node = prompt_entry(id_hint=parent_id)
                root["tactics"].setdefault("items", []).append(parent_node)
                print(f"✅  Created parent '{parent_id}'.")
            else:
                print("Aborted.\n")
                return

    print(f"\nEnter details for new entry under {parent_node['id']}:")
    new_entry = prompt_entry()
    parent_node.setdefault("items", []).append(new_entry)
    print(f"\n✅  Added {new_entry['id']} under {parent_node['id']}\n")


def delete_entry(root: Dict[str, Any]) -> None:
    print("\nCurrent hierarchy:\n")
    print_tree(root["tactics"])
    target_id = input("\nEnter the ID to DELETE (cannot delete root): ").strip()
    if target_id.lower() in ("root", "t0000"):
        print("❌  Cannot delete the root node.\n")
        return
    confirm = input(f"Are you sure you want to delete '{target_id}' and all nested items? (y/n): ").lower()
    if confirm != "y":
        print("Deletion cancelled.\n")
        return

    if remove_node(root["tactics"], target_id):
        print(f"✅  Deleted '{target_id}'.\n")
    else:
        print(f"❌  ID '{target_id}' not found.\n")

########################
# Main interactive loop#
########################

def main():
    file_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("dataset.json")
    data = load_framework(file_path)

    while True:
        print("""
=============================================================================================================
   _____                    _   _   _                              __  __                                   
 |  ___| __ __ _ _   _  __| | | \ | | ___ _   _ _ __ ___  _ __   |  \/  | __ _ _ __   __ _  __ _  ___ _ __ 
 | |_ | '__/ _` | | | |/ _` | |  \| |/ _ \ | | | '__/ _ \| '_ \  | |\/| |/ _` | '_ \ / _` |/ _` |/ _ \ '__|
 |  _|| | | (_| | |_| | (_| | | |\  |  __/ |_| | | | (_) | | | | | |  | | (_| | | | | (_| | (_| |  __/ |   
 |_|  |_|  \__,_|\__,_|\__,_| |_| \_|\___|\__,_|_|  \___/|_| |_| |_|  |_|\__,_|_| |_|\__,_|\__, |\___|_|   
                                                                                           |___/          
=============================================================================================================
1. Show current hierarchy
2. Add new entry (Tactic / Technique / Procedure)
3. Delete entry (and all its children)
4. Save & exit
5. Exit without saving
""")
        choice = input("Select an option [1‑5]: ").strip()

        if choice == "1":
            print("\nCurrent hierarchy:\n")
            print_tree(data["tactics"])
        elif choice == "2":
            add_entry(data)
        elif choice == "3":
            delete_entry(data)
        elif choice == "4":
            save_framework(data, file_path)
            sys.exit(0)
        elif choice == "5":
            print("Exiting without saving…")
            sys.exit(0)
        else:
            print("Invalid option. Please choose 1‑5.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted by user. Goodbye!")
