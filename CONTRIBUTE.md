# Developer's Guide to Contributing

This guide attempts to make no assumptions about the skill level of the developer. Your
contributions are welcome no matter your skill level. If you have questions, you can post
them on the issue tracker (use the appropriate labels so you can get the attention you
need!).

**Communication:**
- [Slack](https://openoakland.slack.com)
- [Issue Tracker](https://github.com/TangoYankee/TrashTalk/issues)

**Development:**
- [Setting up locally](#setting)
- [Code Guidelines](#codeguidelines)
- [Integrations](#integrations)
- [Deployment](#deployment)

## Code Guidelines

- Do not merge your own code. It should be reviewed by your fellow devs and merged by them.
- Test your changes, always, before submitting them.
- Lint your files before submitting them to make sure they follow PEP8
- Never store API keys or passwords in your code! Sensitive data should be stored securely, never in the repository.
- Be sure to add any new modules you install to the requirements file.

**Other Documentation**
- [Flask](http://flask.pocoo.org/docs/0.12/)
- [Python](https://www.python.org/dev/peps/pep-0008/)
- [Google Apps](https://cloud.google.com/docs/)

## Setting Up Local

The steps laid out will be further detailed below, step by step.

1. Fork the main repository
2. Pull the code onto your local machine
3. Set-up your git remotes
4. Create a new branch
5. Commit your changes to the code.
6. Push the branch to your fork
7. Create a Pull Request

Let's get started!

#### Step 1: Create Fork

At the top right of the main repository github page, click the Fork button and save it wherever you like. It should default to your personal account.

Then open your terminal (command line):

```
git clone https://github.com/YOUR_ACCOUNT_HERE/TrashTalk
cd TrashTalk
git remote add upstream https://github.com/openoakland/TrashTalk
```

Now you have forked your own copy of the repo, downloaded the files and set-up your remotes. You're ready to start coding.

#### Step 2: Create a New Branch

Always work on a new branch when developing new changes to the code. Never work on the
master branch.

```
# Update to the latest the code
git pull upstream master

# Create a virtual environment
virtualenv venv
source venv/bin/activate

# Install required modules:
# - Install to local dev:
pip install -r requirements.txt

# - Install for Google Cloud staging:
pip install -t lib -r requirements.txt

# Create and update your database:
echo "create database trashtalk" | mysql -u root -p
alembic upgrade head

# Create a new branch to work on and then start the app
git checkout -b YOUR_BRANCH_NAME
python trashtalk/run.py
```

Update your configuration settings in the following files:
* settings.py: Verify database URI and user settings
* alembic.ini: Check the sqlalchemy.url

Your app should now be running locally. Open your browser to http://localhost:8000 to view it.

You can begin making your changes to the code at this point. Remember to test your changes when you're done to make sure they work.

#### Step 3: Commit and Push

You're done making changes. Now it's time to share your updates.

```
# Verify all the files that have changed
git status

# If you're satisfied, stage all your file changes and additions
git add .

git commit -m "Type a good message here about the changes."
git push origin YOUR_BRANCH_NAME
```

Now go to your fork on Github. You may see a notification about the recent push you just made. Click the "New Pull Request" button next to it.

If you don't see a notification, select YOUR_BRANCH_NAME from the branch drop down menu on the top left of the repository. Then click the "New pull request" button next to it.

Leave a descriptive title and message on your PR. Include links or references to any information that will be helpful to other developers who have to review your code!

The code will be automatically tested by Travis once you create the PR. If you see any test failures, re-review your code and fix the errors. If you're not sure what's wrong, leave a comment on your PR for other devs to help you out.

## Making Model Changes

We use alembic to manage any changes to database tables. It's only partially auto-generated. All changes must be reviewed before committing them.

```
# To run database updates
alembic upgrade head

# Create database changes automatically
alembic revision --autogenerate -m "add new column to users"

# ...Or manually
alembic revision -m "add new column to locations"
```

Once you've create the new migration file go to `migrations/versions` folder and make sure the operations have been generated correctly.

If they are incorrect or imcomplete, here's a guide for adding your changes:
- [Operation Reference](http://alembic.zzzcomputing.com/en/latest/ops.html)
- [Full Documentation](http://alembic.zzzcomputing.com/en/latest/index.html)

