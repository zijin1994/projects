# Project 2

Web Programming with Python and JavaScript

Name: Zijin Gong
Email: zijin@ualberta.ca

In project 2, all server side functions are in application.py, and all the
classes are in models.py. client side DOM designs are in index.html.
Before starting the app, one thing that is important is all the user histories
including user names and last visited channels are stored in localStorage.get('user'),
and localStorage.get('last_channel'), so if there is other app using the same variable
names, make sure to clear them before running the app.

For the personal touch part, i added a delete message button to all the messages that
are sent buy the current user. It gets deleted on server also.
