#!/usr/bin/python3
"""
Read serial raw GNSS data from a device to a file.

Flag arguments:
-of or --outfile: File to write. Default is ~/base_log<datetime>.ubx
-br or --baud_rate: expected baud rate of the device. Default 360800.
-to or --timeout: time in seconds to wait before giving up on a port
-p or --port: name of the port the device is on (don't search)
"""
import sys, os
import argparse

import serial


def make_serial_reader(port, baud_rate, timeout):
    """Create a serial reader for a GNSS receiver."""
    try:
        serial_reader = serial.Serial(
            port="/dev/ttyS0",
            baudrate=460800,
            bytesize=serial.EIGHTBITS,
            timeout=5,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
        )
        return serial_reader
    except Exception as e:
        print(e)
        print("Didn't manage to create a serial reader")


def log_raw_GNSS(serial_reader, outfile):
    """Write binary data from a serial port to a file"""
    if outfile:
        ofname = outfile
    else:
        import time

        timestr = time.strftime("%Y-%m-%d_%H-%H-%S")
        ofname = f"ubx_log_{timestr}.ubx"

    with open(ofname, "wb") as of:
        while True:
            # Using a KiB as a default size; unoptimized
            block = serial_reader.read(1024)
            of.write(block)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("-of", "--outfile", default=None, help="Text file to write data to")
    p.add_argument(
        "-br", "--baud_rate", default=460800, help="expected baud rate of the device"
    )
    p.add_argument(
        "-to", "--timeout", default=5, help="Seconds to wait before giving up on port"
    )
    p.add_argument(
        "-p", "--port", default="/dev/ttyS0", help="Known serial port of device."
    )

    opts = vars(p.parse_args())

    pt = opts["port"]
    br = int(opts["baud_rate"])
    to = int(opts["timeout"])
    of = opts["outfile"]
    print(
        f"\nAttempting to create serial reader with:"
        f"\nbaud rate: {br}"
        f"\non port {pt}"
    )

    reader = make_serial_reader(pt, br, to)
    print(f"Writing output to {of}")
    log_raw_GNSS(reader, of)
