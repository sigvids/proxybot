#!/usr/bin/python3
# -*- coding: utf-8 -*-
''' This module sends Proxy testing results to the Telegram channel '''

import logging
import os
import socket
import datetime
import time
import pytz
import pymysql
from dotenv import load_dotenv
import telegram


def is_open(ip_address, port):
    ''' Test to see if we can connect to a given ip and port '''

    # Create a socket and specify its timeout duration
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)

    # See if we can connect to the given ip and port
    try:
        sock.connect((ip_address, int(port)))
        sock.shutdown(socket.SHUT_RDWR)
        return True
    except:
        return False
    finally:
        sock.close()


def main():
    ''' Test all servers in the Proxy table '''

    # Telegram library uses logging, so set up logging parameters
    logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                        level=logging.INFO)

    # Get the database password, the authorization token, and the chat ID
    load_dotenv()
    database_password = os.getenv("DBPASS")
    authorization_token = os.getenv("AUTHTOKEN")
    chat_id = os.getenv("CHATID")

    # Create the Telegram Bot object
    bot = telegram.Bot(token=authorization_token)

    # Retrieve all Proxy details from the database
    connection = pymysql.connect("localhost", "ProxyBot", database_password,
                                 "ProxyDB")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM `Proxy`")
    results = cursor.fetchall()

    # Iterate around each Proxy server in the database
    for row in results:

        # Get the current time in the UTC time zone
        now = str(pytz.utc.localize(datetime.datetime.utcnow()))[0:19] + " UTC"

        # See if we can make a connection to this Proxy
        if is_open(row[1], row[2]):
            status = "Online at " + now
        else:
            status = "Offline at " + now

        # Send a message to the Telegram channel giving the results
        message_text = row[3] + "\n" + status
        bot.send_message(chat_id=chat_id, text=message_text)

        # Wait a bit to avoid looking like a DDOS or port scanner
        time.sleep(5)


if __name__ == "__main__":
    main()
