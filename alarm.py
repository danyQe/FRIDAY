import re
import datetime
import threading
import time
import sys
from playsound import playsound
import pyttsx3

REMINDERS_FILE = "reminders.txt"
def speak(output):
    engine = pyttsx3.init()
    voices=engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(output)
    engine.runAndWait()
def load_reminders():
    try:
        print("loading reminders from text file....")
        with open(REMINDERS_FILE, "r") as file:
            for line in file:
                parts = line.strip().split(" ", 2)
                print(parts)
                if len(parts) == 3:
                    alarm_datetime=f"{parts[0]} {parts[1]}"
                    message=parts[2]
                    # alarm_datetime_str, message = parts
                    alarm_datetime = datetime.datetime.strptime(alarm_datetime, '%Y-%m-%d %H:%M:%S')
                    alarm_thread = threading.Thread(target=trigger_alarm, args=(alarm_datetime, message))
                    alarm_thread.start()
                else:
                    print("format is wrong in the reminder file")
    except FileNotFoundError:
        print("Reminders file not found.")
def set_alarm(query):
    try:
        # Validate and extract the alarm date, time, and message from the query
        match = re.search(r'\b\d{4}-\d{2}-\d{2} \d{2}:\d{2}\b', query)
        if not match:
            print("Invalid date and time format. Please specify the alarm date and time using the format: 'YYYY-MM-DD HH:MM'.")
            return
        alarm_datetime = datetime.datetime.strptime(match.group(), '%Y-%m-%d %H:%M')
        message = query[match.end():].strip()

        # Validate the alarm datetime
        now = datetime.datetime.now()
        if alarm_datetime < now:
            print("The specified datetime is in the past. Please specify a future datetime.")
            return

        # Write the reminder to the reminders file
        with open(REMINDERS_FILE, "a") as file:
            file.write(f"{alarm_datetime} {message}\n")

        # Schedule the alarm
        alarm_thread = threading.Thread(target=trigger_alarm, args=(alarm_datetime, message))
        alarm_thread.start()

        print(f"Alarm set for {alarm_datetime}: {message}")
    except Exception as e:
        print("Error setting alarm:", str(e))
def trigger_alarm(alarm_datetime, message):
    try:
        while True:
            current_time = datetime.datetime.now()
            if current_time >= alarm_datetime:
                print(f"Alarm: {message}")
                speak(f"Reminder sir:{message}")
                playsound('music.mp3')
                remove_alarm_from_file(alarm_datetime, message)
                # Add code to trigger alarm action (e.g., display message)
                break
            else:
                time.sleep(1)  # Check every second
    except Exception as e:
        print("Error triggering alarm:", str(e))
def remove_alarm_from_file(alarm_datetime, message):
    try:
        reminders = []  # List to store parsed reminders

        # Load existing reminders from the file
        with open(REMINDERS_FILE, "r") as file:
            for line in file:
                parts = line.strip().split(" ", 2)
                if len(parts) == 2:
                    reminder_datetime, reminder_message = parts
                    reminders.append((reminder_datetime, reminder_message))

        # Remove the specified alarm
        updated_reminders = [(r_datetime, r_message) for r_datetime, r_message in reminders if r_datetime != str(alarm_datetime) or r_message != message]

        # Write the updated reminders back to the file
        with open(REMINDERS_FILE, "w") as file:
            for r_datetime, r_message in updated_reminders:
                file.write(f"{r_datetime} {r_message}\n")

        print("Alarm removed:", alarm_datetime, message)
    except FileNotFoundError:
        print("No reminders found.")

# Load reminders from the file and schedule them
args=sys.argv[1:]

if args:
    query=''.join(args)
    print('query received',query)
    set_alarm(query)
else:
    print("no query received\n")
load_reminders()
