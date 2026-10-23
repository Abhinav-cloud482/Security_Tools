Android Recovery Diagnostics

A Python-based diagnostic utility for detecting Android devices through Android Debug Bridge (ADB), checking connection status, retrieving selected system properties, and generating structured JSON reports.

The project is designed to assist with Android device connectivity troubleshooting and authorized recovery diagnostics. It focuses on read-only information gathering and does not attempt to bypass device authentication or modify device security settings.

Table of Contents
Overview
Key Features
Technology Stack
Project Structure
Prerequisites
Installation and Setup
Execution
Diagnostic Workflow
Collected System Properties
Device Connection States
Report Format
Troubleshooting
Security and Limitations
Future Enhancements
Contributing
License
Overview

Android Recovery Diagnostics automates the initial assessment of Android devices connected to a computer through ADB.

The application checks whether ADB is installed, starts the ADB server, discovers connected devices, evaluates their connection states, and retrieves selected system properties from devices with an available ADB shell connection.

The results are displayed in the terminal and saved as a timestamped JSON report for later review.

This tool is intended for developers, technical support personnel, and users performing authorized Android device diagnostics.

Key Features
Device Discovery: Detects Android devices connected through ADB.
Connection State Analysis: Identifies device states such as device, unauthorized, and offline.
System Information Collection: Retrieves the device brand, manufacturer, model, Android version, and security patch level.
Automated Report Generation: Exports diagnostic information to timestamped JSON files.
Error Handling: Handles ADB command failures and subprocess timeouts.
UTC-Based Timestamps: Records report creation times using UTC.
Read-Only Diagnostic Operations: Avoids screen-lock bypass attempts, factory resets, data wipes, and bootloader commands.
Dependency Verification: Checks whether the ADB executable is available before starting diagnostics.
Technology Stack
Technology	Purpose
Python 3.9+	Core application logic
Android Debug Bridge (ADB)	Android device communication
JSON	Structured diagnostic report generation
subprocess	Execution of ADB commands
pathlib	File and directory management
datetime	UTC timestamps
shutil	Verification of ADB availability

The application uses Python standard-library modules and does not require third-party Python packages.

Project Structure
android-recovery-diagnostics/
├── android_recovery.py
├── README.md
└── recovery_reports/
    └── report_YYYYMMDD_HHMMSS.json


File descriptions

android_recovery.py — Main script responsible for device discovery, system property collection, error handling, and report generation.
README.md — Project documentation and usage instructions.
recovery_reports/ — Output directory created automatically when a diagnostic report is saved successfully.

The JSON report files are generated at runtime and do not need to be included in the repository.

Prerequisites

Before running the application, ensure that the following requirements are met:

Python 3.9 or later is installed.
Android SDK Platform Tools are installed.
The adb executable is accessible through the system PATH.
An Android device is connected through USB or another supported ADB connection.
USB debugging is enabled when required.
The connected computer has been authorized for debugging if the device requires authorization.
Verify Python Installation
python --version


On systems that use python3:

python3 --version

Verify ADB Installation
adb version


If the command is unavailable, install Android SDK Platform Tools from the official Android developer website:

https://developer.android.com/tools/releases/platform-tools

Installation and Setup
1. Clone the Repository

Replace YOUR_USERNAME with your GitHub username and use the actual repository name.

git clone https://github.com/YOUR_USERNAME/android-recovery-diagnostics.git

2. Navigate to the Project Directory
cd android-recovery-diagnostics

3. Connect an Android Device

Connect the device to your computer using a data-capable USB cable.

If prompted, approve the USB debugging authorization request on the device.

4. Verify Device Connectivity

Run the following command:

adb devices -l


Review the listed devices and their connection states before proceeding.

Execution

Run the diagnostic script from the project directory.

Windows
python android_recovery.py

Linux and macOS
python3 android_recovery.py


The application checks ADB availability, starts the ADB server, discovers connected devices, collects available diagnostic information, and saves the results to a JSON report.

No additional Python package installation is required.

Diagnostic Workflow

The application follows this sequence during execution:

Dependency Verification: Checks whether the ADB executable is available in the system PATH.
ADB Initialization: Starts the ADB server and verifies that the command completes successfully.
Device Discovery: Executes adb devices -l and parses the detected device entries.
Connection Assessment: Identifies each device's reported ADB state.
Property Collection: Attempts to retrieve selected system properties when the device state is device.
Diagnostic Report Construction: Records device details, available properties, access notes, and diagnostic limitations.
Report Export: Creates the recovery_reports/ directory if necessary and writes the report as a formatted JSON file.
Terminal Output: Displays detected device information, recommended next steps, and the saved report location.

If ADB is unavailable or a critical command fails, the application displays an error message instead of generating a normal diagnostic report.

Collected System Properties

For devices whose ADB state is device, the application attempts to retrieve the following Android system properties.

Report Field	Android Property	Description
brand	ro.product.brand	Product brand
manufacturer	ro.product.manufacturer	Device manufacturer
model	ro.product.model	Device model
android_version	ro.build.version.release	Android release version
security_patch	ro.build.version.security_patch	Android security patch level

If a property cannot be retrieved because of a command failure, timeout, or unavailable value, the report records it as Unavailable.

The collected properties depend on the device and the information exposed through ADB.

Device Connection States

The application interprets ADB connection states to determine which diagnostic actions are appropriate.

Connection State	Description	Recommended Action
device	ADB shell access is available	Review the collected system properties
unauthorized	The computer has not been authorized for ADB access	Approve the debugging prompt if you can unlock and access the device
offline	The device is not responding properly to ADB	Check the USB connection, cable, and debugging availability
Other states	ADB shell access has not been confirmed	Investigate the connection and device configuration

An ADB state of device confirms an available ADB connection; it does not indicate that the Android screen lock has been removed or that all device data is accessible.

Report Format

Each successful execution that reaches the report-writing stage produces a timestamped JSON file in the recovery_reports/ directory.

Output Filename
recovery_reports/report_YYYYMMDD_HHMMSS.json


The timestamp in the filename uses UTC.

Report Fields
Field	Description
created_utc	Report creation timestamp in UTC
purpose	Purpose of the diagnostic operation
devices	List of detected devices and their diagnostic information
notes	Summary of security-related limitations and operations not performed

Each device entry may contain the following fields:

serial — Device serial identifier reported by ADB.
state — ADB connection state.
details — Additional device information reported by ADB.
properties — Selected system properties, when available.
access_note — Guidance based on the reported connection state.
Example JSON Output

The following example illustrates the report structure. Values are placeholders and do not represent an actual device scan.

{
  "created_utc": "2026-10-23T15:00:00+00:00",
  "purpose": "Authorized Android recovery diagnostics",
  "devices": [
    {
      "serial": "ABC123456",
      "state": "device",
      "details": "product:example model:Example_Device",
      "properties": {
        "brand": "ExampleBrand",
        "manufacturer": "ExampleManufacturer",
        "model": "Example_Device",
        "android_version": "14",
        "security_patch": "2024-10-01"
      },
      "access_note": "ADB shell access is available. This does not mean the screen lock is removed."
    }
  ],
  "notes": [
    "This report does not unlock the device.",
    "No PINs, passwords, or authentication tokens are collected.",
    "No reset, wipe, or bootloader commands are issued."
  ]
}


The report contains diagnostic metadata and selected system properties. It does not contain a mechanism for unlocking the device.

Troubleshooting
ADB Is Not Found

Cause: Android SDK Platform Tools are not installed or the ADB executable is not included in the system PATH.

Resolution:

Install Android SDK Platform Tools.
Add the directory containing adb to the system PATH.
Open a new terminal and run adb version.
Execute the Python script again.
No Android Devices Are Detected

Possible causes:

The USB cable does not support data transfer.
USB debugging is disabled.
The device is not connected correctly.
Required USB drivers are missing on Windows.
The device is connected through an unsupported or incorrectly configured connection.

Resolution:

Run:

adb devices -l


Check the connection, USB debugging settings, and device drivers as appropriate.

The Device Is Unauthorized

Cause: The device has not authorized the connected computer for USB debugging.

Resolution: If you can unlock and access the device, approve the USB debugging authorization prompt. If you cannot access the device, this application cannot grant authorization or bypass the requirement.

The Device Is Offline

Cause: ADB cannot currently communicate with the device as expected.

Resolution:

Check the cable and USB connection. If appropriate, restart the ADB server:

adb kill-server
adb start-server
adb devices -l


Then run the diagnostic script again.

System Properties Are Unavailable

Cause: A property query may fail, time out, return an empty value, or be restricted by the device.

Resolution: Confirm that the device is listed with the device state and that ADB shell commands are available. The script records unavailable properties without treating every individual property failure as a fatal error.

The Diagnostic Report Is Not Generated

Possible causes:

ADB initialization or device discovery fails.
A critical ADB command times out.
The application cannot create the output directory.
The output directory is not writable.

Resolution: Review the terminal error message, verify ADB connectivity, and ensure that the project directory is writable.

Security and Limitations

This application is intended for educational, development, and authorized diagnostic purposes.

It does not bypass Android screen locks, PINs, passwords, or account authentication.
It does not collect PINs, passwords, or authentication tokens.
It does not issue factory-reset, data-wipe, or bootloader commands.
It does not exploit Android vulnerabilities or attempt to defeat device security controls.
It retrieves selected system properties only when ADB reports the device state as device.
It cannot guarantee access to a locked device or successful device recovery.
It does not remove the screen lock or modify the device's authentication configuration.
ADB authorization and Android security restrictions remain in effect.

Device serial numbers and connection details may be included in reports. Review generated files before sharing them publicly, and do not commit sensitive diagnostic output to a public repository.

Future Enhancements

Potential improvements for future versions include:

CSV and HTML report export.
Automated diagnostic tests.
Repeated scans and device monitoring.
Configurable command-line arguments.
Improved logging and diagnostic summaries.
Unit tests for device parsing and report generation.
Optional filtering of device identifiers in exported reports.

These are proposed enhancements and are not necessarily implemented in the current version.

Contributing

Contributions, bug reports, and feature suggestions are welcome.

To contribute:

Fork the repository.
Create a feature branch.
Implement and test your changes.
Commit your changes with a descriptive message.
Submit a pull request explaining the changes.

Contributions should preserve the application's authorized, read-only diagnostic scope.

License

This project is licensed under the MIT License.

Disclaimer

Android Recovery Diagnostics is provided for educational, development, and authorized troubleshooting purposes. It is a diagnostic utility, not a screen-lock removal tool or a guarantee of Android device recovery.

The project does not replace official device recovery procedures or manufacturer support. Users are responsible for ensuring they have authorization to diagnose the devices they connect.