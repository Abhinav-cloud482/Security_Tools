
from __future__ import annotations

import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path


REPORT_DIR = Path("recovery_reports")

# Read-only Android system properties.
PROPERTIES = {
    "brand": "ro.product.brand",
    "manufacturer": "ro.product.manufacturer",
    "model": "ro.product.model",
    "android_version": "ro.build.version.release",
    "security_patch": "ro.build.version.security_patch",
}


def run_adb(*args: str, timeout: int = 10) -> str:
    """Execute an ADB command with a timeout."""
    result = subprocess.run(
        ["adb", *args],
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )

    if result.returncode != 0:
        message = result.stderr.strip() or "ADB command failed"
        raise RuntimeError(message)

    return result.stdout.strip()


def discover_devices() -> list[dict[str, str]]:
    """List devices and identify their ADB connection state."""
    output = run_adb("devices", "-l")
    devices = []

    for line in output.splitlines()[1:]:
        line = line.strip()

        if not line or line.startswith("*"):
            continue

        fields = line.split()
        if len(fields) < 2:
            continue

        serial, state = fields[0], fields[1]
        devices.append({
            "serial": serial,
            "state": state,
            "details": " ".join(fields[2:]),
        })

    return devices


def read_properties(serial: str) -> dict[str, str]:
    """Read non-secret system properties from an authorized device."""
    properties = {}

    for name, prop in PROPERTIES.items():
        try:
            value = run_adb(
                "-s", serial, "shell", "getprop", prop
            )
            properties[name] = value or "Unavailable"
        except (RuntimeError, subprocess.TimeoutExpired):
            properties[name] = "Unavailable"

    return properties


def build_report() -> dict:
    if not shutil.which("adb"):
        raise RuntimeError(
            "ADB was not found. Install Android Platform Tools "
            "and add the adb executable to PATH."
        )

    # Check that the ADB server responds.
    run_adb("start-server")

    devices = discover_devices()
    report = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "purpose": "Authorized Android recovery diagnostics",
        "devices": [],
        "notes": [
            "This report does not unlock the device.",
            "No PINs, passwords, or authentication tokens are collected.",
            "No reset, wipe, or bootloader commands are issued.",
        ],
    }

    for device in devices:
        entry = dict(device)

        if device["state"] == "device":
            entry["properties"] = read_properties(
                device["serial"]
            )
            entry["access_note"] = (
                "ADB shell access is available. "
                "This does not mean the screen lock is removed."
            )
        elif device["state"] == "unauthorized":
            entry["access_note"] = (
                "Approve this computer's debugging prompt on the "
                "phone, if you can unlock it."
            )
        elif device["state"] == "offline":
            entry["access_note"] = (
                "Device is offline to ADB. Check the cable, USB "
                "connection, and debugging availability."
            )
        else:
            entry["access_note"] = (
                "ADB shell access is not currently confirmed."
            )

        report["devices"].append(entry)

    return report


def main() -> None:
    try:
        report = build_report()
    except (RuntimeError, subprocess.TimeoutExpired) as exc:
        print(f"[ERROR] {exc}")
        return

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    filename = REPORT_DIR / (
        "report_" +
        datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        + ".json"
    )

    filename.write_text(
        json.dumps(report, indent=2),
        encoding="utf-8",
    )

    if not report["devices"]:
        print("No Android devices detected.")
        print("Check USB, drivers, and USB debugging.")
    else:
        for device in report["devices"]:
            print(
                f"\nDevice: {device['serial']}"
                f"\nState: {device['state']}"
                f"\nDetails: {device['details']}"
                f"\nNext step: {device['access_note']}"
            )

            for key, value in device.get(
                "properties", {}
            ).items():
                print(f"  {key}: {value}")

    print(f"\nDiagnostic report saved to: {filename}")


if __name__ == "__main__":
    main()
