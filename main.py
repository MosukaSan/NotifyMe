from win11toast import toast
from time import sleep
from datetime import datetime
import os
import easygui
import json
import threading
import keyboard
import ctypes

stop_executions = False

def notification_schedule(notification):
    seconds = 0
    executed = False

    while not stop_executions:
        if seconds == 60:
            executed = False

        if datetime.now().strftime("%H:%M") == notification["schedule"] and not executed:
            toast( 
                notification["title"], 
                notification["message"], 
                icon=notification["icon"]
                )
            print("Notification send")
            seconds = 0
            executed = True

        sleep(1)
        seconds += 1
        
def notification_time_range(notification):
    seconds = 0

    while not stop_executions:
        if seconds == notification["time_range"]*60:
            toast( 
                notification["title"], 
                notification["message"], 
                icon=notification["icon"]
                )

            print("Notificação enviada")
            seconds = 0

        sleep(1)
        seconds += 1

def start_notification(notification):
    if notification["schedule"] != None:
        thread = threading.Thread(target=notification_schedule, args=(notification,), daemon=True)
        thread.start()
    elif notification["time_range"] != None:
        thread = threading.Thread(target=notification_time_range, args=(notification,), daemon=True)
        thread.start()

def main():
    ctypes.windll.kernel32.SetConsoleTitleW("NotifyMe")

    notifications = []
    appdata = os.getenv('APPDATA') + "\\NotifyMe\\"

    if os.path.exists(f"{appdata}notifications.json") and os.stat(f"{appdata}notifications.json").st_size != 0:
        with open(f"{appdata}notifications.json", "r", encoding="utf-8") as notifications_file:
            notifications = json.load(notifications_file)

    print("NotifyMe, customize your notifications!")
    sleep(2)

    while True:
        os.system("cls")

        print("--NotifyMe--")
        print("[1] - Create a notification")
        print("[2] - Edit a notification")
        print("[3] - Remove all notifications")
        print("[4] - Start")
        print("[5] - Exit")
        answer = input()

        if answer == "1":
            os.system("cls")

            title = input("Title: ")
            message = input("Message: ")
            want_icon = input("Do you want an icon? (y/n): ")
            image_location = easygui.fileopenbox(msg="Choose an icon", title="File Selection", filetypes=["*.ico", "*.png", "*.jpg", "*.jpeg"]) if want_icon == "y" else os.path.dirname(os.path.abspath(__file__)) + "\\default.png"
            os.system("cls")
            print("[1] - Schedule a time to the notification")
            print("[2] - Define a time range")
            schedule_or_specifc_time = input()
            schedule = input("Choose a time using the 24 hour format (example: 1:00AM -> 1:00, 2:00PM -> 14:00): ") if schedule_or_specifc_time == "1" else None
            time_range = int(input("Choose a time range in minutes: ")) if schedule_or_specifc_time == "2" else None      

            notifications.append({
                "title": title,
                "message": message,
                "icon": image_location,
                "schedule": schedule,
                "time_range": time_range,
            })

            with open(f"{appdata}notifications.json", "w", encoding="utf-8") as notifications_file:
                json.dump(notifications, notifications_file, ensure_ascii=False, indent=4)
        elif answer == "2":
            if notifications:
                os.system("cls")
                iteration = 1
                for notification in notifications:
                    print(f"[{iteration}] {notification}")
                    iteration += 1

                print("\nType '0' to exit")
                answer = int(input("Choose one notification: "))

                if answer > 0:
                    notification = notifications[answer - 1]
                    os.system("cls")

                    print("[1] - Edit")
                    print("[2] - Delete")
                    answer2 = input()

                    if answer2 == "1":
                        iteration2 = 1
                        notification_keys = []
                        for key, value in notification.items():
                            print(f"[{iteration2}] {key}:{value}")
                            notification_keys.append(key)
                            iteration2 += 1

                        answer3 = int(input("Choose one value: "))
                        os.system("cls")
                        notification_keys = notification_keys[answer3 - 1]
                        if isinstance(notifications[answer - 1][notification_keys], str):
                            new_value = input("Insert the new value: ")
                        else:
                            new_value = int(input("Insert the new value: "))
                        notifications[answer - 1][notification_keys] = new_value

                        with open(f"{appdata}notifications.json", "w", encoding="utf-8") as notifications_file:
                            json.dump(notifications, notifications_file, ensure_ascii=False, indent=4)
                    elif answer2 == "2":
                        del notifications[answer - 1]

                        with open(f"{appdata}notifications.json", "w", encoding="utf-8") as notifications_file:
                            json.dump(notifications, notifications_file, ensure_ascii=False, indent=4)

                        print("Deleted")
                        sleep(2)
                elif answer < 0:
                    os.system("cls")
                    print("Choose a valid option! ")
                    sleep(2)
            else:
                os.system("cls")
                print("You don't have any notification registered!")
                sleep(2)
        elif answer == "3":
            os.system("cls")
            notifications = []

            with open(f"{appdata}notifications.json", "w", encoding="utf-8") as notifications_file:
                        json.dump(notifications, notifications_file, ensure_ascii=False, indent=4)

            print("All notifications removed")
            sleep(2)
        elif answer == "4":
            if notifications:
                global stop_executions
                stop_executions = False
                stop_loop = False
                
                def timer_exit():
                    print("Stopping...")
                    nonlocal stop_loop
                    stop_loop = True

                for notification in notifications:
                    start_notification(notification)

                os.system("cls")
                print("Running... (press ctrl+alt+q to stop)")
                keyboard.add_hotkey("ctrl+alt+q", timer_exit)

                while not stop_loop:
                    pass

                keyboard.remove_all_hotkeys()
                stop_executions = True
            else:
                print("No notifications registered")
        elif answer == "5":
            print("Exiting...")
            sleep(2)
            exit()
        else:
            print("Choose a valid option")
            sleep(2)
        
        
if __name__ == "__main__":
    main()
