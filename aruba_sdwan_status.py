#!/usr/bin/env python3
"""
Aruba SD-WAN Orchestrator API Client
Check EdgeConnect device status using the official pyedgeconnect library

Requirements:
    pip install pyedgeconnect
"""

import argparse
import json
import sys
from getpass import getpass
from pyedgeconnect import Orchestrator


def connect_orchestrator(url, username, password, api_key=None, verify_ssl=True):
    """
    Connect to Aruba Orchestrator

    Args:
        url (str): Orchestrator URL (e.g., 'orchestrator.example.com')
        username (str): Admin username
        password (str): Admin password
        api_key (str): Optional API key for authentication
        verify_ssl (bool): Whether to verify SSL certificates

    Returns:
        Orchestrator: Connected Orchestrator instance
    """
    print(f"Connecting to Orchestrator: {url}")

    # Initialize Orchestrator connection
    orch = Orchestrator(url, verify_ssl=verify_ssl)

    # Login with username/password or API key
    if api_key:
        print("Authenticating with API key...")
        orch.api_key = api_key
    else:
        print(f"Logging in as user: {username}")
        orch.login(username, password)

    print("✓ Successfully connected to Orchestrator\n")
    return orch


def get_orchestrator_info(orch):
    """Get Orchestrator system information"""
    try:
        info = orch.get_orchestrator_server_info()
        print("=== Orchestrator Information ===")
        print(f"Version: {info.get('version', 'N/A')}")
        print(f"Release Date: {info.get('releaseDate', 'N/A')}")
        print(f"Server Name: {info.get('serverName', 'N/A')}")
        print()
        return info
    except Exception as e:
        print(f"Error getting orchestrator info: {e}")
        return None


def get_appliance_status(orch, detailed=False):
    """
    Retrieve EdgeConnect appliance status

    Args:
        orch (Orchestrator): Connected Orchestrator instance
        detailed (bool): Whether to fetch detailed appliance information

    Returns:
        list: List of appliances with status information
    """
    try:
        print("=== Retrieving EdgeConnect Appliances ===")
        appliances = orch.get_appliances()

        if not appliances:
            print("No appliances found.")
            return []

        print(f"Found {len(appliances)} appliance(s)\n")

        # Print appliance status
        for idx, appliance in enumerate(appliances, 1):
            print(f"--- Appliance {idx} ---")
            print(f"Hostname: {appliance.get('hostName', 'N/A')}")
            print(f"NE ID: {appliance.get('nePk', 'N/A')}")
            print(f"Model: {appliance.get('model', 'N/A')}")
            print(f"Serial Number: {appliance.get('serial', 'N/A')}")
            print(f"State: {appliance.get('state', 'N/A')}")
            print(f"Reachability: {appliance.get('reachability', 'N/A')}")
            print(f"Software Version: {appliance.get('softwareVersion', 'N/A')}")
            print(f"Site: {appliance.get('site', 'N/A')}")
            print(f"Group: {appliance.get('group', 'N/A')}")

            if detailed:
                print(f"Platform: {appliance.get('platform', 'N/A')}")
                print(f"Deployment Mode: {appliance.get('mode', 'N/A')}")
                print(f"Management IP: {appliance.get('managementIP', 'N/A')}")

            print()

        return appliances

    except Exception as e:
        print(f"Error retrieving appliances: {e}")
        return []


def get_appliance_alarms(orch, ne_pk):
    """
    Get active alarms for a specific appliance

    Args:
        orch (Orchestrator): Connected Orchestrator instance
        ne_pk (str): Network Element Primary Key (appliance ID)

    Returns:
        list: List of active alarms
    """
    try:
        print(f"=== Alarms for Appliance {ne_pk} ===")
        alarms = orch.get_appliance_alarms(ne_pk)

        if not alarms:
            print("No active alarms.")
            return []

        print(f"Found {len(alarms)} active alarm(s)")
        for alarm in alarms:
            print(f"  - {alarm.get('severity', 'N/A')}: {alarm.get('description', 'N/A')}")

        return alarms

    except Exception as e:
        print(f"Error retrieving alarms: {e}")
        return []


def export_to_json(data, filename):
    """Export data to JSON file"""
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"\n✓ Data exported to {filename}")
    except Exception as e:
        print(f"Error exporting to JSON: {e}")


def main():
    parser = argparse.ArgumentParser(
        description='Check Aruba SD-WAN EdgeConnect device status',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage with username/password
  python aruba_sdwan_status.py --url orchestrator.example.com --username admin

  # Use API key authentication
  python aruba_sdwan_status.py --url orchestrator.example.com --api-key YOUR_API_KEY

  # Get detailed information and export to JSON
  python aruba_sdwan_status.py --url orchestrator.example.com --username admin --detailed --export appliances.json

  # Disable SSL verification (not recommended for production)
  python aruba_sdwan_status.py --url orchestrator.example.com --username admin --no-verify-ssl
        """
    )

    parser.add_argument('--url', required=True, help='Orchestrator URL (e.g., orchestrator.example.com)')
    parser.add_argument('--username', help='Admin username')
    parser.add_argument('--password', help='Admin password (will prompt if not provided)')
    parser.add_argument('--api-key', help='API key for authentication (alternative to username/password)')
    parser.add_argument('--detailed', action='store_true', help='Show detailed appliance information')
    parser.add_argument('--no-verify-ssl', action='store_true', help='Disable SSL certificate verification')
    parser.add_argument('--export', metavar='FILE', help='Export appliance data to JSON file')
    parser.add_argument('--check-alarms', action='store_true', help='Check for active alarms on appliances')

    args = parser.parse_args()

    # Validate authentication method
    if not args.api_key and not args.username:
        parser.error("Either --username or --api-key must be provided")

    # Get password if username provided but password not
    password = args.password
    if args.username and not args.password and not args.api_key:
        password = getpass("Enter password: ")

    try:
        # Connect to Orchestrator
        orch = connect_orchestrator(
            url=args.url,
            username=args.username,
            password=password,
            api_key=args.api_key,
            verify_ssl=not args.no_verify_ssl
        )

        # Get Orchestrator information
        get_orchestrator_info(orch)

        # Get appliance status
        appliances = get_appliance_status(orch, detailed=args.detailed)

        # Check alarms if requested
        if args.check_alarms and appliances:
            for appliance in appliances:
                ne_pk = appliance.get('nePk')
                if ne_pk:
                    get_appliance_alarms(orch, ne_pk)
                    print()

        # Export to JSON if requested
        if args.export and appliances:
            export_to_json(appliances, args.export)

        # Logout (if using username/password authentication)
        if not args.api_key:
            orch.logout()
            print("\n✓ Logged out from Orchestrator")

        return 0

    except Exception as e:
        print(f"\n✗ Error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
