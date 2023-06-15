#  Flask app to sort Gmaps results by number of reviews

This app is created in python and use selenium to scrape results from google maps and show them sorted by number of reviews.


# How to deploy:

## Method 1: Local use
Prerequiste: Google chrome installed on system
Steps:
1. Clone this repositary
2. Activate virtual environement in python 

    `$ source venv/bin/activate`

3. Run application.py in your python environment
   
     `$ python3 application.py`

5. Open http://localhost:5000 in web browser.

## Method 2: Delploy on Linux server (Amazon EC2 or Azure)

 - Update server `$ sudo apt update`
 - Install google-chrome
	

		$ sudo apt install wget
		$ wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
		$ sudo dpkg -i google-chrome-stable_current_amd64.deb
		$ sudo apt install 

 - Clone this repo
 - Create service file for app
	 - run `$ sudo nano /etc/systemd/system/gmaps.service`
	 - Add following in file:
		    
		    [Unit]  
		    Description=Gunicorn instance for gmaps app
		    After=network.target
		    
		    [Service]  
		    User=azureuser  
		    Group=www-data  
		    WorkingDirectory=/home/azureuser/gmaps 
		    ExecStart=/home/azureuser/gmaps/venv/bin/gunicorn --timeout 60 -b localhost:8000 application:app  
		    Restart=always
		    
		    [Install]  
		    WantedBy=multi-user.target
 - Run following commads to enable service

	    $ sudo systemctl daemon-reload  
	    $ sudo systemctl start gmaps
	    $ sudo systemctl enable gmaps
Before going to next steps enable public traffic on your server on port 80 and 443. 

 -  Install Nginx —  `$ sudo apt install nginx`
 - Edit server config  file 
 

	    $ sudo nano /etc/nginx/sites-available/default

	-   Add the following code at the top of the file (below the default comments)
	
		    upstream gmaps {  
		        server 127.0.0.1:8000;  
		    }
	    

	 - Add a  `proxy_pass`  to gmaps at`location /`

		    #Some code above
		    location / {  
		    proxy_pass http://gmaps;  
		    }
		    #some code below

 - Start Nginx by using following commands

	    $ sudo systemctl start nginx  
	    $ sudo systemctl enable nginx

Go to your public IP address to see the web app. Use http:// instead of https://.

