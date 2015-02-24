# Project Codename *"stashURLinks"*

## Getting Started

0. ### Install Requirements

  ```bash
  pip install -r requirements.txt
  ```

1. ### Create `secret.py` file

  Copy `stashmarksProj\secret.py.fake` to  `stashmarksProj\secret.py` and set the secret keys

2. ### Update the database

  ```bash
  python manage.py migrate
  ```

3. ### Populate data
  ```
  python populate_db.py
  ```
