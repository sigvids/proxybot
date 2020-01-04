#!/usr/bin/python3
# -*- coding: utf-8 -*-
''' This module sends Proxy connection testing results to the Telegram channel '''

import logging
import telegram
import os
import socket
import pymysql
import datetime
import time
import pytz


def isOpen(ip, port):
    ''' Test to see if we can connect to a given ip and port '''

    # Create a socket and specify its timeout duration
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)

    # See if we can connect to the given ip and port
    try:
        s.connect((ip, int(port)))
        s.shutdown(socket.SHUT_RDWR)
        return True
    except:
        return False
    finally:
        s.close()


def main():

    # Telegram library uses logging, so set up logging parameters
    logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                        level=logging.INFO)

    # Get the database password, the authorization token, and the chat ID
    from dotenv import load_dotenv
    load_dotenv()
    DATABASE_PASSWORD = os.getenv("DBPASS")
    AUTHORIZATION_TOKEN = os.getenv("AUTHTOKEN")
    CHAT_ID = os.getenv("CHATID")

    # Create the Telegram Bot object
    bot = telegram.Bot(token=AUTHORIZATION_TOKEN)

    # Retrieve all Proxy details from the database
    connection = pymysql.connect("localhost", "ProxyBot", DATABASE_PASSWORD,
                                 "ProxyDB")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM `Proxy`")
    results = cursor.fetchall()

    # Iterate around each Proxy server in the database
    for row in results:

        # Get the current time in the UTC time zone
        now = str(pytz.utc.localize(datetime.datetime.utcnow()))[0:19] + " UTC"

        # See if we can make a connection to this Proxy
        if isOpen(row[1], row[2]):
            status = "Online at " + now
        else:
            status = "Offline at " + now

        # Send a message to the Telegram channel giving the results
        message_text = row[3] + "\n" + status
        bot.send_message(chat_id=CHAT_ID, text=message_text)

        # Wait a bit to avoid looking like a DDOS or port scanner
        time.sleep(5)


if __name__ == "__main__":
    main()
