#!/usr/bin/python3
# -*- coding: utf-8 -*-
''' This module prints details of all servers in the Proxy table '''

import os
import pymysql
from dotenv import load_dotenv


def main():
    ''' Print all rows from the Proxy table '''

    # Get the password for the database
    load_dotenv()
    database_password = os.getenv("DBPASS")

    # Retrieve all rows from the Proxy table
    connection = pymysql.connect("localhost", "ProxyBot", database_password,
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
