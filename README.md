# Havoc2Nginx 

havoc2nginx is a simple python script that converts Havoc Framework's yaotl malleable c2 profile to Nginx configuration file format. 

Most of the code and the configuration of this project came from the [`cs2modrewrite` project](https://github.com/threatexpress/cs2modrewrite) from Joe Vest and Andrew Chiles. All credits to them. 

## Usage 
1. Redirector server dependencies 
```
sudo apt install -y nginx nginx-extras
```

2. Run the script
```
python3 havoc2nginx.py  -i ./examples/example.yaotl -c https://127.0.0.1:2222 -r https://www.google.com -H blog.example.com -o ./examples/example.conf
```

3. Relocate the configuration file and restart nginx 
```
sudo cp nginx.conf /etc/nginx/nginx.conf    (or use terraform/ansible...) 
sudo service nginx restart
```

## Help 
```
└─# python3 test.py --help 
usage: test.py [-h] -i INPUTFILE -c C2SERVER -r REDIRECT -H HOSTNAME [-d] [-o OUTPUT]

options:
  -h, --help    show this help message and exit
  -i INPUTFILE  C2 Profile file
  -c C2SERVER   C2 Server URL (e.g., http://teamserver_ip:1337 or https://teamserver_domain)
  -r REDIRECT   Redirect non-matching requests to this URL (https://google.com)
  -H HOSTNAME   Hostname for Nginx redirector
  -d            Include IP Denylist or not. Default False.
  -o OUTPUT     Output filename
```

## Reference & Credits 
- (Script) https://github.com/threatexpress/cs2modrewrite/tree/master
- (Denylist) https://github.com/mgeeky/RedWarden