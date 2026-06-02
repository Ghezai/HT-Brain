# Python Project Setup

Use this guide when creating a new Python project.

## 0. Install Python On Local Machine

Download Python from:

```text
https://www.python.org/downloads/
```

On Windows installation:

1. Run the installer.
2. Check `Add python.exe to PATH`.
3. Click `Install Now`.
4. After install, open a new terminal.

Verify:

```bash
python --version
```

Alternative Windows command:

```bash
py --version
```

Check pip:

```bash
python -m pip --version
```

Upgrade pip:

```bash
python -m pip install --upgrade pip
```

If `python` does not work but `py` works, use:

```bash
py -m pip install --upgrade pip
```

## 0.1 Install VS Code

Download VS Code from:

```text
https://code.visualstudio.com/
```

Recommended VS Code extensions:

```text
Python
Pylance
GitLens
EditorConfig for VS Code
```

Optional extensions:

```text
Ruff
Jupyter
Rainbow CSV
```

## 0.2 Configure Python In VS Code

Open the project folder in VS Code:

```bash
code .
```

Select Python interpreter:

1. Press `Ctrl+Shift+P`.
2. Search `Python: Select Interpreter`.
3. Choose the project virtual environment.

Example interpreter:

```text
.venv\Scripts\python.exe
```

If `.venv` is not listed:

1. Create the virtual environment first.
2. Restart VS Code.
3. Run `Python: Select Interpreter` again.

## 0.3 Configure VS Code Terminal

Open terminal in VS Code:

```text
Terminal -> New Terminal
```

Activate venv manually if needed.

PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Git Bash:

```bash
source .venv/Scripts/activate
```

Verify VS Code terminal is using the venv:

```bash
python -c "import sys; print(sys.executable)"
```

Expected path should include:

```text
.venv
```

## 0.4 Recommended VS Code Settings

Create:

```text
.vscode/settings.json
```

Example:

```json
{
  "python.defaultInterpreterPath": ".venv\\Scripts\\python.exe",
  "python.terminal.activateEnvironment": true,
  "python.analysis.typeCheckingMode": "basic",
  "editor.formatOnSave": true
}
```

For Git Bash users, you can still select Git Bash as the VS Code terminal profile manually from the terminal dropdown.

## 1. Create Project Folder

PowerShell or Git Bash:

```bash
mkdir my-python-project
cd my-python-project
```

You can use any folder name.

Examples:

```text
Migration-DQT
dqc-migration-tools
reporting-tools
api-sync
```

## 2. Initialize Git

```bash
git init
```

Check status:

```bash
git status
```

## 3. Create Virtual Environment

Windows:

```bash
py -m venv .venv
```

Alternative:

```bash
python -m venv .venv
```

This creates:

```text
my-python-project/
  .venv/
```

## 4. Activate Virtual Environment

PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Git Bash:

```bash
source .venv/Scripts/activate
```

After activation, the terminal should show:

```text
(.venv)
```

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Then activate again:

```powershell
.\.venv\Scripts\Activate.ps1
```

## 5. Create Basic Files

PowerShell:

```powershell
New-Item main.py
New-Item requirements.txt
New-Item .gitignore
New-Item README.md
```

Short PowerShell aliases:

```powershell
ni main.py
ni requirements.txt
ni .gitignore
ni README.md
```

Git Bash:

```bash
touch main.py requirements.txt .gitignore README.md
```

## 6. Recommended `.gitignore`

```gitignore
# Python
__pycache__/
*.pyc
*.pyo
*.pyd

# Virtual environment
.venv/
venv/
env/

# Environment variables
.env
.env.local
.env.*
!.env.example

# Test and tooling
.pytest_cache/
.coverage
htmlcov/
.mypy_cache/
.ruff_cache/

# IDE/editor
.vscode/
.idea/

# OS files
.DS_Store
Thumbs.db

# Local data/output
data/*.duckdb
data/*.duckdb.wal
reports/*.csv
reports/*.json
```

## 7. Install Packages

Example:

```bash
python -m pip install pandas duckdb python-dotenv
```

Save installed packages:

```bash
python -m pip freeze > requirements.txt
```

For a new project, prefer writing a clean `requirements.txt` manually when possible:

```txt
pandas
duckdb
python-dotenv
```

Then install:

```bash
python -m pip install -r requirements.txt
```

## 8. Test Python

In `main.py`:

```python
print("Python environment is working")
```

Run:

```bash
python main.py
```

Expected output:

```text
Python environment is working
```

## 9. Recommended Folder Structure

Simple project:

```text
my-python-project/
  .venv/
  main.py
  requirements.txt
  .gitignore
  README.md
```

Data, migration, or testing project:

```text
dqc-migration-tools/
  .venv/
  src/
    __init__.py
    main.py
  config/
  data/
    .gitkeep
  reports/
    .gitkeep
  scripts/
  tests/
  .env
  .env.example
  .gitignore
  README.md
  requirements.txt
```

## 10. `.env` Setup

Use `.env` for local configuration and secrets.

Example `.env.example`:

```env
DUCKDB_PATH=data/app.duckdb
DB_SERVER=
DB_NAME=
DB_USER=
DB_PASSWORD=
```

Create real `.env`.

PowerShell:

```powershell
Copy-Item .env.example .env
```

Git Bash:

```bash
cp .env.example .env
```

Do not commit `.env`.

## 11. Read `.env` In Python

Install:

```bash
python -m pip install python-dotenv
```

Example:

```python
import os

from dotenv import load_dotenv


load_dotenv(".env")

db_server = os.getenv("DB_SERVER")
print(db_server)
```

## 12. Commit First Version

Check files:

```bash
git status
```

Add and commit:

```bash
git add .
git commit -m "Initial Python project setup"
```

Make sure `.env` and `.venv/` are not staged.

## Common Commands

Activate venv in PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Activate venv in Git Bash:

```bash
source .venv/Scripts/activate
```

Install requirements:

```bash
python -m pip install -r requirements.txt
```

Run app:

```bash
python main.py
```

Check installed packages:

```bash
python -m pip list
```

Update requirements:

```bash
python -m pip freeze > requirements.txt
```

Deactivate venv:

```bash
deactivate
```
