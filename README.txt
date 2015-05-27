Hello, this application was built by Henrique Calixto in order to attend to the third project
of the Full Stack Web Developer course at Udacity.com

The project's objective is to make an application that provides a list of items within a variety
of categories as well as provide a user registration and authentication system. Registered users
will have the ability to post, edit and delete their own items.

 The project is composed by the following files:
 	1)database_setup.py: the database schema and declaration using sqlalchemy.
 	2)dbInterface: this module is composed of python functions that interact with the database
 	in all the ways needed for this aplication.
 	3)client_secret.json and fb_client_screts.json: configuration files needed to log in using
 	  google plus and facebook accounts
 	4)project.py: the main application file containing the instructions to deal with the server
 	  requests using the flask frame-work
 	5)templates folder: contain the html template (main.html) that is the visual part of the application
 	6)static folder: contain the javascript files responsables for the interface and log in and the css
 	  file responsable for the style of the application

 To run this application:
 	1)Install Vagrant (https://www.vagrantup.com/) and VirtualBox (https://www.virtualbox.org/)
 	2)Clone the fullstack-nanodegree-vm repository (https://github.com/udacity/fullstack-nanodegree-vm)
 	3)Replace the content of the tournament folder (fullstack\vagrant\tournament) with this application's content
 	4)Launch the Vagrant VM
 	5)Run the database_setup.py to instal the application database.
 	6)Run the project.py file to start the application at http://localhost:5000