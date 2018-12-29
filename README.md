# Catalog Project

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
That'll create the tables and test data. To start the web app then execute:
```
$ python application.py
```
The web server starts listening on <a href="http://localhost:8000">http://localhost:8000</a>. You should be able to navigate through the sample data.

The app implements a json endpoint at <a href="http://localhost:8000/catalog.json">http://localhost:8000/catalog.json</a> which will serve the same information available at the HTML endpoints 

#### Setting up Google API  

Before login into the app, you need to create the Google Auth credentials:

* Go to your app's page in the Google APIs Console — https://console.developers.google.com/apis
* Choose Credentials from the menu on the left.
* Create an OAuth Client ID.
* This will require you to configure the consent screen.
* When you're presented with a list of application types, choose Web application.
* You will then be able to get the client ID and client secret.

Download the client secret as a JSON data file once you have created the credentials and replace the _client_secrets.json_ file found on the root folder of the app.


**Project Status**
```
Submitted
```