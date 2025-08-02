import socket
import re

# Read the server list from infosserver.txt
with open("infosserver.txt", "r") as f:
    server_list = f.read().splitlines()

# Extract hostnames from the server list
hostnames = []
for line in server_list:
    match = re.search(r"name: '([^']*)'", line)
    if match:
        hostnames.append(match.group(1))

# Check the status of each server
server_status_list = []
for server in hostnames:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    try:
        result = sock.connect_ex((server, 443))
        if result == 0:
            server_status_list.append((server, 'online'))
        else:
            server_status_list.append((server, 'offline'))
    except socket.gaierror:
        server_status_list.append((server, 'offline'))
    finally:
        sock.close()

# Read the HTML layout template
with open("layout.txt", "r") as f:
    layout_template = f.read()

# Generate the HTML content
html_content = ""
for server, status in server_status_list:
    html_content += f"<p>{{server}}: {{status}}</p>\n"

# Create the final HTML
final_html = layout_template.replace('{content}', html_content)

# Write the final HTML to a file
with open('server_status.html', 'w') as f:
    f.write(final_html)