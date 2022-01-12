# Bundesliga_Website

### Pre-run requirements

 - A postgresql deployment
 - Python version 3.8+


### Running Setup

The commands used may differ depending on operating system. The ones below
are for a windows machine not running any Linux shell underneath

```
git clone git@github.com:Sunchasing/Bundesliga_Website.git

cd Bundesliga_Website

python3 -m venv venv/

venv/Scripts/activate.bat

python -m pip install -r requirements.txt

cd Bundesliga

copy NUL Bunesliga/secret.py

```

At this point, you should add two Python variables to that file. You can also add logic to get these files from
something like AWS Secrets Manager or env vars:

1. `DJANGO_SECRET = 'somerandomsecureunguessablestring123'`
2. `DB_Password = 'the_password_for_db_user'`


```
python manage.py migrate

python manage.py runserver
```

The first time you run the server, you need to send a GET Request to the /v1/update endpoint
in order to load your DB with all the latest information.


Endpoints:
 - /v1/matches/ - Displays all upcoming matches for the current season.
 - /v1/teams/ - Displays all teams active in the current season.
 - /v1/teams/{id}/ - Replacing {id} with the team_id in DB will get a team's statistics for the current season.
 - /uptime/ - Displays how long the server has been up for.
 - /v1/update/ - Updates the local database with the contents of the remote API backend. This can be done once every 10 minutes.
