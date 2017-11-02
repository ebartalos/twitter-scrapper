import os


def notify(title, text):
    os.system("""
              osascript -e 'display notification "%s" with title "%s"'
              """ % (text, title))


notify("Title", "Heres an alert")
