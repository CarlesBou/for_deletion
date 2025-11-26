# Aruba SD-WAN Orchestrator API Setup Guide

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements_aruba.txt
```

Or install directly:
```bash
pip install pyedgeconnect
```

### 2. Basic Usage

**With Username/Password:**
```bash
python aruba_sdwan_status.py --url orchestrator.example.com --username admin
```

**With API Key:**
```bash
python aruba_sdwan_status.py --url orchestrator.example.com --api-key YOUR_API_KEY
```

### 3. Advanced Options

**Get Detailed Information:**
```bash
python aruba_sdwan_status.py --url orchestrator.example.com --username admin --detailed
```

**Check Active Alarms:**
```bash
python aruba_sdwan_status.py --url orchestrator.example.com --username admin --check-alarms
```

**Export to JSON:**
```bash
python aruba_sdwan_status.py --url orchestrator.example.com --username admin --export appliances.json
```

**Disable SSL Verification (for self-signed certificates):**
```bash
python aruba_sdwan_status.py --url orchestrator.example.com --username admin --no-verify-ssl
```

## Getting API Key from Orchestrator

1. Login to your Orchestrator web interface with admin credentials
2. Navigate to: **Support → API Key**
3. Generate or copy your existing API key
4. Use it with the `--api-key` parameter

## What Information Can You Get?

The script retrieves:

- **Appliance Details:**
  - Hostname
  - Model & Serial Number
  - Software Version
  - State & Reachability status
  - Site & Group information
  - Management IP

- **Orchestrator Information:**
  - Version
  - Release Date
  - Server Name

- **Alarms (optional):**
  - Active alarms for each appliance
  - Severity levels
  - Alarm descriptions

## API Documentation

Access the full REST API documentation directly from your Orchestrator:
1. Login to Orchestrator
2. Go to **Support → REST APIs**
3. Browse Swagger documentation

## Authentication Methods

### Username/Password
- Requires login/logout for each session
- More suitable for interactive scripts
- Automatically handled by the script

### API Key
- No need for login/logout
- Better for automation and scheduled tasks
- Set up in Orchestrator UI

## Troubleshooting

### SSL Certificate Errors
If you encounter SSL errors with self-signed certificates:
```bash
python aruba_sdwan_status.py --url orchestrator.example.com --username admin --no-verify-ssl
```

### Connection Timeout
- Ensure the Orchestrator URL is correct
- Check network connectivity
- Verify firewall rules allow API access

### Authentication Errors
- Verify username/password or API key
- Check user has appropriate permissions (admin role recommended)
- Ensure API access is enabled in Orchestrator

## Python API Usage Example

For custom integrations, you can use the library directly:

```python
from pyedgeconnect import Orchestrator

# Initialize and connect
orch = Orchestrator('orchestrator.example.com', verify_ssl=True)
orch.login('admin', 'password')

# Get all appliances
appliances = orch.get_appliances()

# Get specific appliance info
ne_pk = appliances[0]['nePk']
appliance_detail = orch.get_appliance(ne_pk)

# Get alarms
alarms = orch.get_appliance_alarms(ne_pk)

# Logout
orch.logout()
```

## Resources

- **Official Python Library**: [pyedgeconnect on GitHub](https://github.com/aruba/pyedgeconnect)
- **PyPI Package**: [pyedgeconnect on PyPI](https://pypi.org/project/pyedgeconnect/)
- **Developer Hub**: [Aruba Developer Portal](https://developer.arubanetworks.com/edgeconnect/docs/)
- **API Endpoints**: [Orchestrator and EdgeConnect API Reference](https://developer.arubanetworks.com/edgeconnect/docs/aruba-orchestrator-and-edgeconnect-api-endpoints)

## Next Steps

1. Install the library: `pip install pyedgeconnect`
2. Get your Orchestrator URL and credentials
3. Run the script to check device status
4. Explore the API documentation for additional capabilities

For production use, consider:
- Using API keys instead of username/password
- Implementing proper error handling
- Adding logging for auditing
- Scheduling regular status checks
- Integrating with monitoring systems
