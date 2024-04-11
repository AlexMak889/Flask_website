from flask import Flask, render_template
import mariadb

conn = mariadb.connect(
        user="Alex",
        password="alexmak889",
        host="192.168.1.63",
        database="temp"
    )