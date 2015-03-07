# Project Codename *"stashURLinks"*

## Requirements

- Python 3.4
- Django 1.7.4

## Getting Started

0. ### Setup virtual environment _(optional)_

  ```bash
  mkvirtualenv stashurlinks
  ```

1. ### Install Requirements

  ```bash
  pip install -r requirements.txt
  ```

2. ### Create `secret.py` file

  Copy `stashmarksProj/secret.py.fake` to  `stashmarksProj/secret.py` and set the secret keys

  ```bash
  cp ./stashmarksProj/secret.py.fake ./stashmarksProj/secret.py
  nano ./stashmarksProj/secret.py
  ```

3. ### Update the database

  ```bash
  python manage.py migrate
  ```

4. ### Populate sample data
  ```
  python populate_db.py
  ```

## Login
  ### Default users

  - Username: `user1` Password: `pass`
  - Username: `user2` Password: `pass`
  - Username: `user3` Password: `pass`
  - Username: `admin` Password: `pass`

### Social login

To login with social account you must set correct keys in `secret.py`.
