# Docker container for Flask, Nginx, and uWSGI, + Letsencrypt's certbot-auto for HTTPS

## Purpose:
Provide Dockerfile and all applicable config and base Flask scripts necessary to start a webpage, with a script to automate HTTPS re-configuration.

## Why do I use it?:
(Be sure docker is installed.  If not installed, run install_docker.sh) <br>

With this container and a built image (or pulling the image from ucnt/flaskwebpage), you can get an HTTP or HTTPS server setup in 1 commands
- HTTP: sudo docker run -d -p 80:80 -p 443:443 --restart=always -t --name flaskwebpage flaskwebpage <br>
- HTTPS (change parameters): sudo docker run -d -p 80:80 -p 443:443 --restart=always -t --name flaskwebpage flaskwebpage "-d example.com,www.example.com -n example.com -e my@email.com" <br>

Notes: 
- If you arleady setupt he server as HTTP and you want HTTPS, run: /home/flask/conf/setup-https.py -d [domain_list_csv] -n [certname] -e [email_address]
- You can access the container via: sudo docker exec -i -t flaskwebpage /bin/bash

## More thoughts:
https://www.mattsvensson.com/nerdings/2017/6/30/docker-flasknginxuwsgi

## Notes/Details:
<ul>
  <li><b>Folder/File Sctructure</b></li>
  <ul>
    <li>All of the files+folders in this repo will be, by default, put into /home/flask.  If you modify this you need to update the Dockerfile.</li>
    <li>The /home/flask/app folder will contain the Flask app.  As long as the wsgi.py file uses "app" not "application," you can swap in and out any flask app that you want (so long as you have the necessary libraries installed).</li>
  </ul>
  
  <br>
  
  <li><b>Services/Notes</b></li>
  <ul>
    <li>This script uses linux's Supervisor to monitor and control uWSGI and nginx.</li>
    <li>Port 443 is left on the run command in case you want to use it.  If you never will, you can remove "-p 443:443"</li>
</ul>  

  <br>

  <li><b>HTTPS Setup Options (assumes 1 domain per container instance)</b></li>
  <ul>
  <li><b>Do it the easy way!</b> Go into the container and run a command like one of the below examples to automate the setup via a custom script I wrote.  Before running it, yes, <b>you should own the domain and have updated the DNS records</b>.</li>
      - /home/flask/conf/setup-https.py -d test.com -n test.com -e test@test.com
      <br>
      - /home/flask/conf/setup-https.py -d test.com,www.test.com -n test.com -e test@test.com
      <br>
    <li>Do it the hard way: 
      <br>
    - If you want to use Let's Encrpyt: Run "/home/flask/certbot-auto certonly -d [YOURDOMAIN] -w /home/flask/app" or else copy your existing certs to the folder of your choice.
      <br>
    - Adjust /home/flask/conf/nginx-https-template.conf to use HTTPS by replacing YOURDOMAIN with the domain you are setting up and, if you copied a cert into a folder, change the directory from /etc/letsencrpyt/live
      <br>
    - Remove /etc/nginx/sites-enabled/nginx-http.conf
      <br>
    - Re-link ntinx-https.conf to /etc/nginx/sites-enabled: ln -s /home/flask/conf/nginx-https-template.conf /etc/nginx/sites-enabled/nginx-http.conf
      <br>
    - Restart the supervisor service</li>
  </ul>  
  
  <br>
  
  <li><b>Credits</b></li>
  <ul>
    <li>Credit to Thatcher Peskens (https://github.com/atupal/dockerfile.flask-uwsgi-nginx), who this code was forked from.</li>
  </ul>  

</ul>


