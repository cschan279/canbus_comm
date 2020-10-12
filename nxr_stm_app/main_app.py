from ui import app
import configparser
c = configparser.ConfigParser()
c.read('usb.ini')


win = app.App(dev=c['USB']['PORT'])

win.mainloop()
x = input('Enter to Quit')
