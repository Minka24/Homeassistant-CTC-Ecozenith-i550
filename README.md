# README for CTC Ecozenith i550 Integration

## Overview

This integration allows Home Assistant to communicate with the CTC Ecozenith i550 heat pump over Modbus. It provides a seamless way to monitor and control the heat pump from within the Home Assistant ecosystem.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/ctc_ecozenith_i550.git
   ```

2. **Copy the integration folder**:
   Copy the `ctc_ecozenith_i550` folder to your Home Assistant `custom_components` directory.

3. **Restart Home Assistant**:
   After copying the files, restart your Home Assistant instance to load the new integration.

## Configuration

To configure the CTC Ecozenith i550 integration, follow these steps:

1. Go to **Settings** in Home Assistant.
2. Navigate to **Devices & Services**.
3. Click on **Add Integration** and search for "CTC Ecozenith i550".
4. Enter the required information:
   - **Name**: A name for your heat pump.
   - **Host**: The IP address of the heat pump.
   - **Port**: The Modbus port (default is usually 502).

## Usage

Once configured, the integration will automatically fetch data from the heat pump. You can create sensor entities in Home Assistant to monitor various parameters such as temperature, humidity, and operational status.

## Development

If you wish to contribute to this integration, please follow these guidelines:

- Ensure your code adheres to the Home Assistant coding standards.
- Write tests for any new features or changes.
- Submit a pull request with a clear description of your changes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.