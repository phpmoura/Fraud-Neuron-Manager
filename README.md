# Fraud Framework Updater

Interactive CLI helper for maintaining the **Fraud Tactics‑Techniques‑Procedures (TTP) JSON framework** used in threat‑fraud mapping projects.

---

## ✨ Key Features

| Capability | Description |
|------------|-------------|
| **Auto‑load / create** | Looks for `fraudneuron.json` in the current directory and builds a fresh skeleton if missing or corrupted. |
| **Browse hierarchy** | Pretty‑prints the tree so you can visualise Tactics, Techniques, and Procedures. |
| **Add nodes** | Insert new Tactics (`T*`), Techniques (`TQ*`), or Procedures (`P*`) anywhere in the tree. |
| **Parent validation** | If you reference a parent ID that doesn’t exist, the tool offers to create it on‑the‑fly. |
| **Delete nodes** | Remove any node (and all its children) by ID—root is protected. |
| **Safe save** | Pretty‑prints JSON with UTF‑8 and 2‑space indent. |

---

## 🖥️ Prerequisites

* Python ≥ 3.8

No third‑party packages required—everything uses the standard library.

---

## 🚀 Quick Start

```bash
# 1) Clone your repo and cd in
$ git clone https://github.com/your‑org/your‑repo.git
$ cd your‑repo

# 2) Run the updater (creates fraudneuron.json if missing)
$ python fraud_framework_updater.py
```

> **Tip**  You can pass a different JSON file as the first argument:
>
> ```bash
> $ python fraud_framework_updater.py my_other_framework.json
> ```

---

## 🧭 Menu Walk‑through

```
==========================
 Fraud Framework Updater
==========================
1. Show current hierarchy
2. Add new entry (Tactic / Technique / Procedure)
3. Delete entry (and all its children)
4. Save & exit
5. Exit without saving
```

### 1 — Show current hierarchy

Prints a tree view, e.g.

```
T0000 — tactics
  ├─ T1000 — target_identification
  │   └─ TQ1100 — target_types
  │       └─ P1111 — consumers
  └─ T2000 — themes
```

### 2 — Add new entry

1. Choose the **parent ID** (or type `root` to add a new Tactic).
2. If the ID doesn’t exist you can create it.
3. Enter the **ID**, **title**, and **description** for the new node.

> IDs are not enforced but convention is:
>
> * `T*`   → Tactic
> * `TQ*` → Technique (can nest multiple levels)
> * `P*`   → Procedure

### 3 — Delete entry

* Provide the ID you wish to remove (everything nested is also deleted).
* Root (`T0000`) is protected.

### 4 — Save & exit

Writes the in‑memory tree back to the JSON file and quits.

### 5 — Exit without saving

Discard changes.

---

## 🗂 File Structure

```
├─ fraud_framework_updater.py   # the CLI tool
└─ fraudneuron.json             # the framework (auto‑generated)
```

---

## 🔄 Example Session

```text
$ python fraud_framework_updater.py

==========================
 Fraud Framework Updater
==========================
1. Show current hierarchy
2. Add new entry (Tactic / Technique / Procedure)
3. Delete entry (and all its children)
4. Save & exit
5. Exit without saving

Select an option [1‑5]: 2

Parent ID (or 'root' for top‑level): T2000

Enter details for new entry under T2000:
  > New ID: TQ2300
  > Title: charity_schemes
  > Description: Exploiting fake charities for donation fraud

✅  Added TQ2300 under T2000
```

---

## 🤝 Contributing

1. Fork the repo & create a feature branch.
2. Keep code **PEP‑8 compliant** and document new functions.
3. Open a PR—maintainers will review.

---

## 📄 License

This project is licensed under the **Apache 2.0 License**—see `LICENSE` for details.
