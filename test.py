#!/usr/bin/python3
# -*- coding: utf-8 -*-
''' This module tests proxies and displays the results on the terminal '''

import os
import socket
import pymysql
import datetime
import time
import pytz


def isOpen(ip, port):

    # Create a socket and specify a timeout duration
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)

    # See if we can open a connection to the given ip and port
    try:
        s.connect((ip, int(port)))
        s.shutdown(socket.SHUT_RDWR)
        return True
    except:
        return False
    finally:
        s.close()


def main():

    # Get the password for the database
    from dotenv import load_dotenv
    load_dotenv()
    DATABASE_PASSWORD = os.getenv("DBPASS")

    # Retreive all the Proxy details from the Proxy table
    connection = pymysql.connect("localhost", "ProxyBot", DATABASE_PASSWORD,
                                 "ProxyDB")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM `Proxy`")
    results = cursor.fetchall()

    for row in results:

        # Get the current time in UTC time zone
        now = str(pytz.utc.localize(datetime.datetime.utcnow()))[0:19] + " UTC"

        # Set status depending on whether or not we can connect to the Proxy
        if isOpen(row[1], row[2]):
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
