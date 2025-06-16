import sys
import time
from urllib.parse import urlparse

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


    
