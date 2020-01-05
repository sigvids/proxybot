#!/usr/bin/python3
# -*- coding: utf-8 -*-
''' This module tests proxies and displays the results on the terminal '''

import os
import socket
import datetime
import time
import pytz
import pymysql
from dotenv import load_dotenv


def is_open(ip_address, port):
    ''' See if ip address and port are open for connections '''

    # Create a socket and specify a timeout duration
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)

    # See if we can open a connection to the given ip and port
    try:
        sock.connect((ip_address, int(port)))
        sock.shutdown(socket.SHUT_RDWR)
        return True
    except:
        return False
    finally:
        sock.close()


def main():
    ''' Loop round all servers in the Proxy table '''

    # Get the password for the database
    load_dotenv()
    database_password = os.getenv("DBPASS")

    # Retrieve all the Proxy details from the Proxy table
    connection = pymysql.connect("localhost", "ProxyBot", database_password,
                                 "ProxyDB")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM `Proxy`")
    results = cursor.fetchall()

    for row in results:

        # Get the current time in UTC time zone
        now = str(pytz.utc.localize(datetime.datetime.utcnow()))[0:19] + " UTC"

        # Set status depending on whether or not we can connect to the Proxy
        if is_open(row[1], row[2]):
            status = "Online at " + now
        else:
            status = "Offline at " + now

        # Display this Proxy's status on the terminal
        print("ProxyID: ", row[0])
        print("Host: ", row[1])
        print("Port: ", row[2])
        print("Message: ", row[3])
        print(status, "\n")

        # Wait a bit to avoid looking like a DDOS or port scanner
        time.sleep(5)


if __name__ == "__main__":
    main()
