# improved-fishstick

### Description
This is a REST Api built with Flask. It is a User management system with CRUD operations.

### DEpendencies
* Flask
* PyMongo
* Docker
* Python 3.10+

_Instructions to run_

On the terminal execute the below command to create the projects' working directory and move into that directory.
 
```python
$ mkdir flask_ums
cd flask_ums
```

In the projects' working directory execute the below command to create a virtual environment for our project. Virtual environments make it easier to manage packages for various projects separately.

 
```python
$ virtualenv venv
```

To activate the virtual environment, execute the below command.

```python
$ source venv/Script/activate
```
Clone this repository in the projects' working directory by executing the command below.

```python
$ git clone https://github.com/ajaoooluseyi/flask-ums.git
$ cd flask-ums
```

To install all the required dependencies execute the below command.

```python
$ pip install -r requirements.txt
```

To run the app, navigate to the app folder in your virtual environment and execute the below command
```python
$ FLASK_APP = app

$ FLASK_ENV = development

$ flask run 
```
To build app Docker Image:
```cmd
$ docker build -t flask-mongo-app .
```
Once the image is built, run the Docker container using the following command:
```cmd
docker run -d -p 5000:5000 --name flask-mongo-container flask-mongo-app
```
