# Module 9 — FastAPI + PostgreSQL + pgAdmin

## Overview

This module sets up a FastAPI calculator application backed by a PostgreSQL database, with pgAdmin for database management. All services run via Docker Compose.

---

## Services

| Service | URL | Credentials |
|---|---|---|
| FastAPI | http://localhost:8000 | — |
| FastAPI Docs | http://localhost:8000/docs | — |
| pgAdmin | http://localhost:5050 | `admin@example.com` / `admin` |
| PostgreSQL | `localhost:5432` | user: `postgres`, pass: `postgres`, db: `fastapi_db` |

---

## Quick Start

```bash
docker compose up --build
```

To reset volumes (fresh database):

```bash
docker compose down -v
docker compose up --build
```

---

## Database Schema

### users
| Column | Type | Notes |
|---|---|---|
| id | SERIAL | Primary Key |
| username | VARCHAR(50) | Unique |
| email | VARCHAR(100) | Unique |
| created_at | TIMESTAMP | Default: now() |

### calculations
| Column | Type | Notes |
|---|---|---|
| id | SERIAL | Primary Key |
| operation | VARCHAR(20) | e.g. add, divide |
| operand_a | FLOAT | — |
| operand_b | FLOAT | — |
| result | FLOAT | — |
| timestamp | TIMESTAMP | Default: now() |
| user_id | INTEGER | FK → users(id) ON DELETE CASCADE |

The tables are automatically created when the container starts via `sql/init.sql`.

---

## SQL Scripts

All scripts are in the `sql/` folder and should be run in pgAdmin against `fastapi_db`.

| File | Step | Description |
|---|---|---|
| `sql/init.sql` | Auto | Runs on container first start — creates tables |
| `sql/A_create_tables.sql` | A | Manual CREATE TABLE statements |
| `sql/B_insert_records.sql` | B | Insert alice, bob, and 3 calculations |
| `sql/C_query_data.sql` | C | SELECT users, SELECT calculations, JOIN |
| `sql/D_update_record.sql` | D | UPDATE result of calculation id=1 to 6 |
| `sql/E_delete_record.sql` | E | DELETE calculation id=2, verify with SELECT |

---

## pgAdmin Screenshots

### Step A — Create Tables

<img width="1919" height="981" alt="Screenshot 2026-04-07 200757" src="https://github.com/user-attachments/assets/c9a8bb66-a8fb-4a5c-bc09-4a2405d04ea9" />

Runs `A_create_tables.sql` in pgAdmin. The error `relation "users" already exists` is expected — `init.sql` automatically created the tables when the PostgreSQL container first started, demonstrating that the Docker Compose setup correctly initializes the schema on startup.

---

### Step B — Insert Records

<img width="1919" height="995" alt="Screenshot 2026-04-07 200559" src="https://github.com/user-attachments/assets/279a09db-6da5-4cc9-8a9e-04cc09e34b1e" />

Inserts users `alice` and `bob`, then inserts 3 calculation records (`add`, `divide`, `multiply`) linked via `user_id` foreign key. Query returned successfully in 67 ms.

---

### Step C — Query Data (JOIN)
<img width="1918" height="964" alt="Screenshot 2026-04-07 200042" src="https://github.com/user-attachments/assets/64810b65-b9f5-4368-9b55-f824aebd63da" />


Shows the JOIN between `users` and `calculations` returning 6 rows with username, operation, operands, and result.

---

### Step D — Update Record
<img width="1540" height="946" alt="Screenshot 2026-04-07 200112" src="https://github.com/user-attachments/assets/c74c9dd6-3f3b-4f62-a755-0803b1469a08" />


Updates `result` of calculation `id=1` from `5` to `6`. The verification SELECT confirms the change.

---

### Step E — Delete Record
<img width="1840" height="983" alt="Screenshot 2026-04-07 200137" src="https://github.com/user-attachments/assets/b05a90ef-865f-44c8-a9dd-05bab79380c6" />


Deletes calculation `id=2` (the `divide` operation). The verification SELECT shows 5 remaining rows.

---

# 📦 Project Setup

---

# 🧩 1. Install Homebrew (Mac Only)

> Skip this step if you're on Windows.

Homebrew is a package manager for macOS.  
You’ll use it to easily install Git, Python, Docker, etc.

**Install Homebrew:**

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**Verify Homebrew:**

```bash
brew --version
```

If you see a version number, you're good to go.

---

# 🧩 2. Install and Configure Git

## Install Git

- **MacOS (using Homebrew)**

```bash
brew install git
```

- **Windows**

Download and install [Git for Windows](https://git-scm.com/download/win).  
Accept the default options during installation.

**Verify Git:**

```bash
git --version
```

---

## Configure Git Globals

Set your name and email so Git tracks your commits properly:

```bash
git config --global user.name "Your Name"
git config --global user.email "your_email@example.com"
```

Confirm the settings:

```bash
git config --list
```

---

## Generate SSH Keys and Connect to GitHub

> Only do this once per machine.

1. Generate a new SSH key:

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

(Press Enter at all prompts.)

2. Start the SSH agent:

```bash
eval "$(ssh-agent -s)"
```

3. Add the SSH private key to the agent:

```bash
ssh-add ~/.ssh/id_ed25519
```

4. Copy your SSH public key:

- **Mac/Linux:**

```bash
cat ~/.ssh/id_ed25519.pub | pbcopy
```

- **Windows (Git Bash):**

```bash
cat ~/.ssh/id_ed25519.pub | clip
```

5. Add the key to your GitHub account:
   - Go to [GitHub SSH Settings](https://github.com/settings/keys)
   - Click **New SSH Key**, paste the key, save.

6. Test the connection:

```bash
ssh -T git@github.com
```

You should see a success message.

---

# 🧩 3. Clone the Repository

Now you can safely clone the course project:

```bash
git clone <repository-url>
cd <repository-directory>
```

---

# 🛠️ 4. Install Python 3.10+

## Install Python

- **MacOS (Homebrew)**

```bash
brew install python
```

- **Windows**

Download and install [Python for Windows](https://www.python.org/downloads/).  
✅ Make sure you **check the box** `Add Python to PATH` during setup.

**Verify Python:**

```bash
python3 --version
```
or
```bash
python --version
```

---

## Create and Activate a Virtual Environment

(Optional but recommended)

```bash
python3 -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate.bat  # Windows
```

### Install Required Packages

```bash
pip install -r requirements.txt
```

---

# 🐳 5. (Optional) Docker Setup

> Skip if Docker isn't used in this module.

## Install Docker

- [Install Docker Desktop for Mac](https://www.docker.com/products/docker-desktop/)
- [Install Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)

## Build Docker Image

```bash
docker build -t <image-name> .
```

## Run Docker Container

```bash
docker run -it --rm <image-name>
```

---

# 🚀 6. Running the Project

- **Without Docker**:

```bash
python main.py
```

(or update this if the main script is different.)

- **With Docker**:

```bash
docker run -it --rm <image-name>
```

---

# 📝 7. Submission Instructions

After finishing your work:

```bash
git add .
git commit -m "Complete Module X"
git push origin main
```

Then submit the GitHub repository link as instructed.

---

# 🔥 Useful Commands Cheat Sheet

| Action                         | Command                                          |
| ------------------------------- | ------------------------------------------------ |
| Install Homebrew (Mac)          | `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"` |
| Install Git                     | `brew install git` or Git for Windows installer |
| Configure Git Global Username  | `git config --global user.name "Your Name"`      |
| Configure Git Global Email     | `git config --global user.email "you@example.com"` |
| Clone Repository                | `git clone <repo-url>`                          |
| Create Virtual Environment     | `python3 -m venv venv`                           |
| Activate Virtual Environment   | `source venv/bin/activate` / `venv\Scripts\activate.bat` |
| Install Python Packages        | `pip install -r requirements.txt`               |
| Build Docker Image              | `docker build -t <image-name> .`                |
| Run Docker Container            | `docker run -it --rm <image-name>`               |
| Push Code to GitHub             | `git add . && git commit -m "message" && git push` |

---

# 📋 Notes

- Install **Homebrew** first on Mac.
- Install and configure **Git** and **SSH** before cloning.
- Use **Python 3.10+** and **virtual environments** for Python projects.
- **Docker** is optional depending on the project.

---

# 📎 Quick Links

- [Homebrew](https://brew.sh/)
- [Git Downloads](https://git-scm.com/downloads)
- [Python Downloads](https://www.python.org/downloads/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [GitHub SSH Setup Guide](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)
