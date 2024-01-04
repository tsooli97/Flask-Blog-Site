# My Flask Blog
<img src="https://i.imgur.com/5G1pD7j.png" alt="Image of blog screen">

#### This Flask blog project is a web application where users can read and create blog posts, and comment on them. It's built using Flask, which is a lightweight WSGI web application framework. The blog features user authentication, post creation and admin functionalities. You can check out the live website here: https://tsooli97-flask-blog.onrender.com/
(**NOTE**: Sometimes the website isn't immediately accessible because the instance will spin down after certain period of inactivity, due to the free hosting plan that I've chosen for the project. The website usually comes back up after a couple of page refreshes and a little bit of waiting, to allow the server instance to start up again. Sorry for the inconvenience!)

## Features
### User Authentication: 
Enables users to register, log in, comment on blog posts, and log out. <br><br>
<img src="https://i.imgur.com/SR7SvKy.png" alt="Register screen"> <br><br>
<img src="https://i.imgur.com/8WK5MKD.png" alt="Login screen"> <br><br>
<img src="https://i.imgur.com/55hxdOY.png" alt="Comment screen"> <br><br>

<hr>

### Blog Post Creation: 
Allows admin users to create blog post content and edit it. <br><br>
<img src="https://i.imgur.com/zOOC6M6.png" alt="Image of blog post"> <br><br>
<img src="https://i.imgur.com/XjN1IFL.png" alt="Image of blog post"> <br><br>

<hr>

### Admin Control Panel: 
Admin users can manage the comment permissions of user accounts. <br><br>
<img src="https://i.imgur.com/pxxuH54.png" alt="Image of admin panel"> <br><br>

<hr>

### Responsive Design: 
The application is styled with Bootstrap4, making it responsive and accessible on various devices. <br><br>
<img src="https://i.imgur.com/HYjwyHG.png" alt="Mobile view"> <br><br>

## Requirements
- Python 3.x
- Flask and other dependencies as listed in requirements.txt <br>
Install using `
  
## Usage
You can either try the web application from the standpoint of a normal user on the website:
https://tsooli97-flask-blog.onrender.com/ <br><br>
OR <br><br>
You can run the project locally, in which case you get to try it from the perspective of both an admin and a normal user. To run the project locally:
- Follow the installation steps in the next section, to download the project files on your local machine
- Run `main.py` to start the application
- Access the web application via a web browser at `http://localhost:5000`
- Register as a new user (first user to register becomes admin in this build)
- Start exploring by creating posts, commenting on them or using the admin functionalities if you're an admin user
  
## Installation
- Download the project files .zip or clone the repository to your local machine with the following command (requires Git to be installed): <br>
`git clone https://github.com/tsooli97/Flask-Blog-Site.git`
- Navigate to your project directory by using the command: `cd path/to/your/project`
- Create a virtual environment with the command: `python -m venv <env_name>`
- After creating the environment, activate it with the command: `<env_name>\Scripts\activate`
- Finally, install the packages from requirements.txt by using the command: `pip install -r requirements.txt`
- After you're done, you can deactive the venv with the command: `deactivate`

## Project Structure
- `main.py` The main script to run the Flask application. It includes route definitions and configurations
- `models.py` Contains SQLAlchemy database models for the application
- `forms.py` Defines WTForms for handling forms in the application
- `templates/` Contains HTML templates for rendering the views
- `static/` Contains static files like CSS for styling

## Contributing
Contributions to the project are always welcome. If you're interested in contributing, please feel free to make a pull request or create an issue.
