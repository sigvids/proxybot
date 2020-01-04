#!/usr/bin/python3
# -*- coding: utf-8 -*-
''' This module prints details of all proxies in the proxy table '''

import os
import pymysql


def main():

    # Get the password for the database
    from dotenv import load_dotenv
    load_dotenv()
    DATABASE_PASSWORD = os.getenv("DBPASS")

    # Retrieve all rows from the Proxy table
    connection = pymysql.connect("localhost", "ProxyBot", DATABASE_PASSWORD,
                                 "ProxyDB")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM `Proxy`")
    results = cursor.fetchall()

    for row in results:
        # For each Proxy, print its details from the Proxy table

        print("ProxyID: ", row[0])
        print("Host: ", row[1])
        print("Port: ", row[2])
        print("Message: ", row[3], "\n")


if __name__ == "__main__":
    main()
