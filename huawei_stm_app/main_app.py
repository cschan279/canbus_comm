from ui import app
import configparser
c = configparser.ConfigParser()
c.read('usb.ini')
dev=c['USB']['PORT']
print("Connect via", dev)
win = app.App(dev=dev)

win.mainloop()
x = input('Enter to Quit')
