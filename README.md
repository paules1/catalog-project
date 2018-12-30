# Car Catalog Project

The project consist on creating a _web application_ to manage a cars for sale catalog. Users can freely navigate the catalog, but will need a Google account to login, post, edit, or delete their own listings. 

#### Installation

If you are using MacOS or Windows, you can use <a href="https://www.vagrantup.com/downloads.html">Vagrant</a>
and <a href="https://www.virtualbox.org/">Virtual Box</a> to setup a local Linux environment.
Follow the instructions according to your operating system and complete Vagrant and Virtual Box installations.

Clone the repository on your local machine. On the root folder you'll find the Vagrant configuration file ready to install everything you need on the virtual server. 
    
At the terminal or command prompt window execute these 2 commands (first one might take a few minutes to complete):
 ```
$ vagrant up
$ vagrant ssh
```
Once you run the last command you'll be at the command prompt of your virtual linux box.
Move to the /catalog/app folder, and execute:
```
$ cd /catalog/app
$ python setup.py
```
That'll create the tables and initial data. To start the web server then execute:
```
$ python application.py
```
The web server will start listening on <a href="http://localhost:8000">http://localhost:8000</a>.

####JSON Endpoint
The app implements a json endpoint at <a href="http://localhost:8000/catalog.json">http://localhost:8000/catalog.json</a> which will serve the same information available at the HTML endpoints 

#### Setting up Google API  

To enable the Login functionality the follow these steps:

* Create a Google account if you don't have one.
* Navigate to <a href="https://console.developers.google.com/apis/dashboard">https://console.developers.google.com/apis/dashboard</a>
* Select/Create a project
* From the project's menu select APIs and Services
* Choose Credentials from the menu on the left.
* Press the Create Credentials button and select Create OAuth Client ID.
* Select Web Application from the Application Type options.
* Type a name for the App and add http://localhost:8000 to the Authorized JavaScript origins.  
* A popup with the client id and secret key will appear. Press Ok.
* The new OAuth id will appear on the list.
* Press the download button to download the client_secret.json
* Rename the file to client_secrets.json and use it to replace the existing file located on the /app folder of the repository.

The app is now ready to connect to Google.


**Project Status**
```
Submitted
```