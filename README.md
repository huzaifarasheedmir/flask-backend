# flask-backend

Backend rest server with [Flask](http://flask.pocoo.org/)

## About project
I will be developing and updating a fully functional backend server with complete test coverage and environment deployment support using docker and ansible.

> Please note: This is work in progress series of commits. I will be updating table of content containing commit ids so that you can switch to any update/version of the project using the commit id.

To clone the repo use :
```
git clone https://github.com/huzaifarasheedmir/flask-backend.git
```
If you have already cloned the branch and want to fetch latest updates use 
```
git fetch
git rebase -i origin/master
```
> Please note: There are different techniques of getting latest code you can use rebase, merge and pull study about them on git.

for switching to any commit copy the commit id from below table and use
```
git checkout <commit id>
```
or undo all local changes and go to a commit
```
git reset --hard <commit id>
```
#### Contents


| Commit # |    Commit titile               | Commit id |
|------|---------------------------|---------|
| 1  | [Setup basic app structure](https://github.com/huzaifarasheedmir/flask-backend/commit/0101924667b75e45ba1a6f9cd2e0cf1124a996c3)|0101924667b75e45ba1a6f9cd2e0cf1124a996c3|
| 2  | [Introduce db in app and create user model](https://github.com/huzaifarasheedmir/flask-backend/commit/316c330367bf388215ff1e91c1fd9c720ddbd4ef)|316c330367bf388215ff1e91c1fd9c720ddbd4ef|
| 3  | [Introduce basic user apis in app](https://github.com/huzaifarasheedmir/flask-backend/commit/HEAD)|HEAD|

## Getting started

1. Install python package management tool pip

  ```
    sudo apt-get install python-pip
  ```

2. If you want to work in virtual env follow this or skip to step 3

  ```
    sudo easy_install virtualenv
    virtualenv flaskserver
    cd flaskserver
    source bin/activate
  ```
3. Go to project directory and install require packages using

  ```
    sudo pip install --upgrade -r requirements.txt
  ```
4. Run the server

  ```
    python manage.py runserver
  ```
6. Run tests
  
  * without coverage
  ```
    python manage.py test
  ```
  * with coverage
  ```
    python manage.py test --coverage
  ```