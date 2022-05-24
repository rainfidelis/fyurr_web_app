Fyyur
-----

## Introduction

Fyyur is a musical venue and artist booking site that facilitates the discovery and bookings of shows between local performing artists and venues. This site lets you list new artists and venues, discover them, and list shows with artists as a venue owner.

## Overview

Fyurr aims to be the best platform for artists and musical venues to find each other, and for regular users to discover new music shows. 

To that end, the app allows users to:

* List new venues, artists, and shows
* Search for venues and artists 
* Learn more about a specific venue or artist
* Learn about both past and upcoming shows for artists and venues

## Tech Stack (Dependencies)

### 1. Backend Dependencies

The backend tech stack includes the following:
* **Python3** and **Flask** as the server language and server framework
 * **Pipenv** for creating an isolated Python environment
 * **SQLAlchemy ORM** as the ORM library for database interaction
 * **PostgreSQL** as the database of choice
 * **Flask-Migrate** for creating and running schema migrations
 * **Flask-WTF** for interactively designing python forms

You can download and install the dependencies mentioned above using `pip` as:
```
pip install virtualenv
pip install SQLAlchemy
pip install postgres
pip install Flask
pip install Flask-Migrate
```

### 2. Frontend Dependencies

The application frontend is served using **HTML**, **CSS**, and **Javascript**, along with [Bootstrap 3](https://getbootstrap.com/docs/3.4/customize/). If you're looking to recreate this on your local machine, you'd need to install the Node Package Manager (NPM) to enable installation of Bootstrap on your CLI. If you do not already have it, you can download and install the [Node.js](https://nodejs.org/en/download/). 

> **Note:** Windows users must run the executable as an Administrator, and restart the computer after installation. After successfully installing the Node, verify the installation as shown below.
```
node -v
npm -v
```
Install [Bootstrap 3](https://getbootstrap.com/docs/3.3/getting-started/) for the website's frontend using:
```
npm init -y
npm install bootstrap@3
```

## Main Files: Project Structure

  ```sh
  ├── README.md
  ├── app.py *** The main driver of the app with endpoints and controllers
  ├── config.py *** Database URLs, CSRF generation, etc
  ├── error.log
  ├── forms.py *** Form configurations and management
  ├── models.py *** Models configuration for the database
  ├── requirements.txt *** The python dependencies for the backend
  ├── static
  │   ├── css 
  │   ├── font
  │   ├── ico
  │   ├── img
  │   └── js
  └── templates
      ├── errors
      ├── forms
      ├── layouts
      └── pages
  ```

## Next Steps

The following functionalities are in the works for the application:

* Show Recent Listed Artists and Recently Listed Venues on the homepage, returning results for Artists and Venues sorting by newly created. Limit to the 10 most recently listed items.
* Implement Search Artists by City and State, and Search Venues by City and State. Searching by "San Francisco, CA" should return all artists or venues in San Francisco, CA.
<br><br>
> *This projectt was developed and submitted as part of the Udacity Full Stack Nanodegree Program*