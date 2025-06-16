import sys
import time
import ssl
import socket
from urllib.parse import urlparse
from datetime import datetime

def read_domains_from_file(filename):
    """READ DOMAIN FROM TEXT FILE FUNCTION"""
    domains = []
    try:
        with open(filename, 'r', encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith('#'):
                    if line.startswith(('http://', 'https://')):
                        domain = urlparse(line).netloc
                    else:
                        domain = line
                    domains.append(domain)
    except FileNotFoundError:
        print(f"[ERR]: File {filename} not found!")
        sys.exit(1)
    except Exception as e:
        print(f"[ERR]: Error while reading file: {e}")
        sys.exit(1)
    
    return domains

def get_ssl_expiry_date(domain, port=443):
    """GET INFO ABOUT SSL EXPIRATION DATE"""
    try:
        context = ssl.create_default_context()

        #Establishment connection
        with socket.create_connection((domain, port), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                expiry_date = cert['NotAfter']
                expiry_datetime = datetime.strptime(expiry_date, '%b %d %H:%M:%S %Y %Z')
                return expiry_datetime.strftime('%Y-%m-%d %H:%M:%S')
    
    except socket.gaierror:
        return "[ERR]: Cannot resolve domain name"
    except socket.timeout:
        return "[ERR]: Connection timeout"
    except ssl.SSLError as e:
        return f"[ERR_SSL]: {str(e)}"
    except Exception as e:
        print (f"[ERR]: {str(e)}")
    
