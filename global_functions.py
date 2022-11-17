"""
Module to contain generic functions that I can call on each DES.
"""

from tkinter import messagebox
import login_module
import client_module
import datetime
import pyodbc
import gspread
from oauth2client.service_account import ServiceAccountCredentials

current_user = []

def on_closing():
    """
    Global function used on each DES to make sure user doesnt miss-click the quit button. Allows updates the logs.
    """
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                      'Server=RORYS-PC;'
                      'Database=Users;'
                      'UID=remote_connection;'
                      'PWD=123;')
        conn.execute("UPDATE users SET is_online = 0 WHERE USERNAME='%s'" % current_user[0])
        conn.commit()
        with open("logs.txt", "a+") as text_file:
            text_file.write(f"{datetime.datetime.now()}: {current_user[0]} logged out.\n")
        login_module.login_screen.destroy()

def open_chat():
    client_module.chat_room_window()

def upload_to_sheets(file):
    """
    Uploads file to Google Sheets after user uploads a file to the application. Using file as a parameter so I can use on each DES.
    https://docs.google.com/spreadsheets/d/1fAnJDuyyQTBWd7PLCOANK886cgSIgCEz2iExld1o91s/edit#gid=191967681
    """
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
            "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

    credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(credentials)

    spreadsheet = client.open('tkinter-upload')

    with open(file) as file_obj:
        content = file_obj.read()
        client.import_csv(spreadsheet.id, data=content)
