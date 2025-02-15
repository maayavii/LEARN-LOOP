# LEARN LOOP

a web application that help peer to peer knowledge shering among students in a department

## Features :

<li>Sign Up, Login, google auth, Logout, Forgot Password</li>
<li>Public Profile view</li>
<li>Create, Edit, Delete Posts with customized text, pictures and links</li>
<li>Like, Comment / Reply, and Search posts</li>
<li>Follow and Unfollow users to view their posts</li>
<li>Admin support</li>
<li>Notifications</li>
<li>Video Calls using Agora to conduct group meetings  enabled with screen shereing</li>
<li>Document convertor</li>
<li>document editor</li>
<li>buy me a coffie to support creators</li>
<li>list out the top contributors every month</li>
<li>mock exam creation and attending </li>


## Adding env variables

- Add env variables to ".test.env" and rename it to ".env"

- Add GOOGLE_RECAPTCHA_SECRET_KEY to both .env and the file mentioned below https://github.com/Ronik22/Django_Social_Network_App/blob/main/users/templates/users/register.html#L45

- Add agora app_id to .env and to https://github.com/Ronik22/Django_Social_Network_App/blob/main/blog/static/blog/js/streams.js#L2

## Installation

```bash
    $ python -m venv venv
    $ source venv/Scripts/activate
    (venv) pip install -r requirements.txt
    (venv) cd Django_Social_Network_App
    (venv) python manage.py makemigrations
    (venv) python manage.py migrate
    (venv) python manage.py createsuperuser
    (venv) python manage.py runserver
```


## Add django-allauth config

https://django-allauth.readthedocs.io/en/latest/installation.html#post-installation

## Others

- To use other DB edit this https://github.com/Ronik22/Django_Social_Network_App/blob/main/myproject/settings.py#L107
- To use other providers edit this https://github.com/Ronik22/Django_Social_Network_App/blob/main/myproject/settings.py#L205
- To use redis instead edit this https://github.com/Ronik22/Django_Social_Network_App/blob/main/myproject/settings.py#L197

## Running Tests

To run tests, run the following command

```bash
  python manage.py test
```

