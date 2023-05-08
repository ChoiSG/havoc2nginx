import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument('-i', dest='inputfile', help='C2 Profile file', required=True)
parser.add_argument('-c', dest='c2server', help='C2 Server URL (e.g., http://teamserver_ip:1337 or https://teamserver_domain)', required=True)
parser.add_argument('-r', dest='redirect', help='Redirect non-matching requests to this URL (https://google.com)', required=True)
parser.add_argument('-H', dest='hostname', help='Hostname for Nginx redirector', required=True)
parser.add_argument('-d', dest='denylist', help='Include IP Denylist or not. Default False.', type=bool, action=argparse.BooleanOptionalAction, default=False)
parser.add_argument('-o', dest='output', help='Output filename', required=False)

args = parser.parse_args()

# Debug 
print(f"[DEBUG] Input file: {args.inputfile}")
print(f"[DEBUG] C2 Server: {args.c2server}")
print(f"[DEBUG] Redirect: {args.redirect}")
print(f"[DEBUG] Hostname: {args.hostname}\n")

profile = open(args.inputfile, "r")
contents = profile.read() 

# Regex patterns 
hosts_pattern = r'Hosts\s+=\s+\[(.+?)\]'
user_agent_pattern = r'UserAgent\s+=\s+\"(.+?)\"'
uris_pattern = r'Uris\s+=\s+\[(.+?)\]'

try: 
    hosts_match = re.search(hosts_pattern, contents, re.DOTALL)
    user_agent_match = re.search(user_agent_pattern, contents, re.DOTALL)
    uris_match = re.search(uris_pattern, contents, re.DOTALL)

except Exception as e:
    print(f"[-] Error: {str(e)}")

if hosts_match is None:
    print("[-] Error: Hosts not found")
    exit()
if user_agent_match is None:
    print("[-] Error: UserAgent not found")
    exit()
if uris_match is None:
    print("[-] Error: Uris not found")
    exit()

# Parse and populate host, ua, uris_string
try:
    hosts_raw = hosts_match.group(1)
    hosts = [host.strip().strip('"') for host in hosts_raw.split(',')]
    if len(hosts) == 1:
        hosts = hosts[0]

    user_agent = user_agent_match.group(1)
    
    uris_raw = uris_match.group(1)
    uris = [uri.strip().strip('"') for uri in uris_raw.split(',')]
    uris_string = ".*|".join(uris) + ".*"

except Exception as e:
    print(f"[-] Error: {str(e)}")

# DEBUG 
print(f"[DEBUG] Hosts: {hosts}")
print(f"[DEBUG] hosts type: {type(hosts)}")
print(f"[DEBUG] User-Agent: {user_agent}")
print(f"[DEBUG] URIs: {uris}")
print(f"[DEBUG] URIs string: {uris_string}\n")

# Import nginx, denylist template 
with open('nginx-template.conf','r') as f:
    nginx_template = f.read()

if args.denylist:
    with open('denylist-template.conf','r') as f:
        denylist = f.read()
        denylist = "\n".join(["        " + line for line in denylist.split("\n")])
else:
    denylist = "# NO DENYLIST" 

# Update template files 
nginx_template = nginx_template.format(uris=uris_string, user_agent=user_agent, c2server=args.c2server, redirect=args.redirect, hostname=args.hostname, denylist=denylist)

print(nginx_template)

if args.output is not None:
    with open(args.output, "w") as f:
        f.write(nginx_template)
    print(f"\n[+] Nginx configuration file wrote to: {args.output}")