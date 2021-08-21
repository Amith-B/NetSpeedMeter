import threading
import time
import psutil
from tkinter import Tk,Label,Button,OptionMenu,StringVar,NORMAL,DISABLED,PhotoImage
from tkinter.messagebox import showinfo
import os
import sys

speedUp=None
speedDown=None
bgr='black'
alpha=.9
run=True
interface=[itf for itf in list(dict.keys(psutil.net_if_stats())) if(psutil.net_if_stats()[itf].isup)][0]
interface_list_at_startup=[itf for itf in list(dict.keys(psutil.net_if_stats())) if(psutil.net_if_stats()[itf].isup)]
buttonSelectInterface=None
windowx=0
windowy=0

if(len(interface)==0):
    os._exit(0)

if(os.path.exists('C:\\ProgramData\\NetSpeed\\netinterfacedata.log')):
    with open('C:\\ProgramData\\NetSpeed\\netinterfacedata.log','r') as f:
       line=str(f.readline()).strip()
       interfacelist=[itf for itf in list(dict.keys(psutil.net_if_stats())) if(psutil.net_if_stats()[itf].isup)]
       if(line in interfacelist):
           if(psutil.net_if_stats()[interface].isup):
               interface=line
           else:
               interface=interfacelist[0]
       else:
           interface=interfacelist[0]


def speedCalc(up,down,timediff=1):
    global speedUp,speedDown,run,interface,interface_list_at_startup,buttonSelectInterface
    up=0
    down=0
    while(run):
        try:
            if(interface in list(dict.keys(psutil.net_if_stats()))):
                if(not psutil.net_if_stats()[interface].isup):
                    interface_list_new=[itf for itf in list(dict.keys(psutil.net_if_stats())) if(psutil.net_if_stats()[itf].isup)]
                    previnter=interface
                    interface=list(set(interface_list_new).difference(interface_list_at_startup))[0] if(len(list(set(interface_list_new).difference(interface_list_at_startup)))>0) else interface
                    
                    if(previnter!=interface):
                        buttonSelectInterface.config(text=interface[0])
                        interface_list_at_startup=[itf for itf in list(dict.keys(psutil.net_if_stats())) if(psutil.net_if_stats()[itf].isup)]
                        if(path.exists('C:\\ProgramData\\NetSpeed')):
                            with open('C:\\ProgramData\\NetSpeed\\netinterfacedata.log','w+') as f:
                                f.write(interface)
                        else:
                            os.mkdir('C:\\ProgramData\\NetSpeed')
                            with open('C:\\ProgramData\\NetSpeed\\netinterfacedata.log','w+') as f:
                                f.write(interface)
                    continue
                    #on_closing()
            else:
                interface_list_new=[itf for itf in list(dict.keys(psutil.net_if_stats())) if(psutil.net_if_stats()[itf].isup)]
                previnter=interface
                interface=list(set(interface_list_new).difference(interface_list_at_startup))[0] if(len(list(set(interface_list_new).difference(interface_list_at_startup)))>0) else interface
                
                if(previnter!=interface):
                    buttonSelectInterface.config(text=interface[0])
                    interface_list_at_startup=[itf for itf in list(dict.keys(psutil.net_if_stats())) if(psutil.net_if_stats()[itf].isup)]
                    
                    if(os.path.exists('C:\\ProgramData\\NetSpeed')):
                        with open('C:\\ProgramData\\NetSpeed\\netinterfacedata.log','w+') as f:
                            f.write(interface)
                    else:
                        os.mkdir('C:\\ProgramData\\NetSpeed')
                        with open('C:\\ProgramData\\NetSpeed\\netinterfacedata.log','w+') as f:
                            f.write(interface)
                continue
            
            sent=psutil.net_io_counters(pernic=True)[interface].bytes_sent
            recv=psutil.net_io_counters(pernic=True)[interface].bytes_recv
            total=(sent+recv)/1000
            unitUp=1
            unitDown=1
            unitTotal=1
            upspeed=(sent-up)/1000
            downspeed=(recv-down)/1000
            if(len(str(int(upspeed)))>=4):
                upspeed=upspeed/1000
                unitUp=2
            if(len(str(int(downspeed)))>=4):
                downspeed=downspeed/1000
                unitDown=2
            if(len(str(int(total)))>=7):
                total=total/1000000
                unitTotal=3
            elif(len(str(int(total)))>=4):
                total=total/1000
                unitTotal=2
            
            speedUp.config(text='{0:.2f} {1}/s'.format(upspeed,'KB' if unitUp==1 else 'MB'))
            speedDown.config(text='{0:.2f} {1}/s'.format(downspeed,'KB' if unitDown==1 else 'MB'))
            totalUsage.config(text='{0:.2f} {1}'.format(total,'KB' if unitTotal==1 else 'MB' if unitTotal==2 else 'GB'))
            time.sleep(timediff)
            up=sent
            down=recv
        except Exception as e:
            pass


def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def getnetinterface():
    global buttonSelectInterface,interface,bgr,windowx,windowy,interface_list_at_startup
    
    w=175
    h=30
    x = windowx
    y = windowy
    if(x<0 or y<0):
        x,y=0,0
    netinterface = Tk()
    netinterface.title("Select Network Interface")
    netinterface.geometry('%dx%d+%d+%d' % (w, h, x, y))
    netinterface.wm_attributes('-alpha',alpha)
    netinterface.wm_attributes('-topmost', 1)

    var = StringVar(netinterface)
    var.set("Select Network Interface")

    def grab_and_assign(event):
       global buttonSelectInterface,interface,bgr,interface_list_at_startup
       chosen_option = var.get()
       interface=chosen_option
       if(os.path.exists('C:\\ProgramData\\NetSpeed')):
           with open('C:\\ProgramData\\NetSpeed\\netinterfacedata.log','w+') as f:
               f.write(interface)
       else:
           os.mkdir('C:\\ProgramData\\NetSpeed')
           with open('C:\\ProgramData\\NetSpeed\\netinterfacedata.log','w+') as f:
               f.write(interface)
       buttonSelectInterface.config(text=interface[0])
       interface_list_at_startup=[itf for itf in list(dict.keys(psutil.net_if_stats())) if(psutil.net_if_stats()[itf].isup)]
       netinterface.destroy()
    lst=[itf for itf in list(dict.keys(psutil.net_if_stats())) if(psutil.net_if_stats()[itf].isup)]
    drop_menu = OptionMenu(netinterface, var,*lst, command=grab_and_assign)
    drop_menu.config(bg=bgr,fg='white')
    drop_menu.grid(row=0, column=0)

    netinterface.resizable(0, 0)
    netinterface.overrideredirect(1)
    netinterface.configure(background=bgr)
    
    netinterface.mainloop()





app=Tk()
xpos,ypos=0,0
butBool=False
totalBool=False
upBool=False
downBool=False
downiconBool=False
totaliconbool=False
interfacebuttonbool=False
infobuttonbool=False
def on_closing():
    global app,run
    run=False
    app.destroy()
    os._exit(0)
def move_window(event):
    global xpos,ypos,butBool,totalBool,upBool,downBool,downiconBool,totaliconbool,windowx,windowy,interfacebuttonbool,infobuttonbool
   
    if(not butBool and not interfacebuttonbool and not infobuttonbool):
        if(totalBool):
            app.geometry(f'+{event.x_root-xpos-27}+{event.y_root-ypos-50}')
            windowx=event.x_root-xpos-27
            windowy=event.y_root-ypos-50
        elif(totaliconbool):
            app.geometry(f'+{event.x_root-xpos}+{event.y_root-ypos-50}')
            windowx=event.x_root-xpos
            windowy=event.y_root-ypos-50
        elif(upBool):
            app.geometry(f'+{event.x_root-xpos-27}+{event.y_root-ypos}')
            windowx=event.x_root-xpos-27
            windowy=event.y_root-ypos
        elif(downBool):
            app.geometry(f'+{event.x_root-xpos-27}+{event.y_root-ypos-25}')
            windowx=event.x_root-xpos-27
            windowy=event.y_root-ypos-25
        elif(downiconBool):
            app.geometry(f'+{event.x_root-xpos}+{event.y_root-ypos-25}')
            windowx=event.x_root-xpos
            windowy=event.y_root-ypos-25
        else:
            app.geometry(f'+{event.x_root-xpos}+{event.y_root-ypos}')
            windowx=event.x_root-xpos
            windowy=event.y_root-ypos
    butBool=False
    totalBool=False
    upBool=False
    downBool=False
    downiconBool=False
    totaliconbool=False
    interfacebuttonbool=False
    infobuttonbool=False



def showInfo():
    showinfo('Info', 'The interface selected is: \n\"'+interface+'\"\n\nIf you want to change the interface, click on the letter which is below the close button')
def getorigin(eventorigin):
    global xpos,ypos
    xpos = eventorigin.x
    ypos = eventorigin.y
def buttonmotion(event):
    global butBool
    butBool=True
def totalUsagemotion(event):
    global totalBool
    totalBool=True
def speedUpmotion(event):
    global upBool
    upBool=True
def speedDownmotion(event):
    global downBool
    downBool=True
def speedDowniconmotion(event):
    global downiconBool
    downiconBool=True
def totaliconmotion(event):
    global totaliconbool
    totaliconbool=True
def interfacebuttonmotion(event):
    global interfacebuttonbool
    interfacebuttonbool=True
def infomotion(event):
    global infobuttonbool
    infobuttonbool=True
    
# change the transperancy when mouse is scrolled
def scrollmouse(event):
    global alpha
    if(event.delta<0):
        if(alpha>.15):
            alpha=alpha-.05
            app.wm_attributes('-alpha',alpha)
    else:
        if(alpha<1.0):
            alpha=alpha+.05
            app.wm_attributes('-alpha',alpha)
#close window
def exitNetspeed():
    global app,run
    run=False
    app.destroy()
    os._exit(0)



app.title('Net Speed')
w=160
h=76
# get screen width and height
ws = app.winfo_screenwidth() # width of the screen
hs = app.winfo_screenheight() # height of the screen

# calculate x and y coordinates for the Tk root window
x = ws-w
y = hs-116
windowx=x
windowy=y
app.geometry('%dx%d+%d+%d' % (w, h, x, y))
app.wm_attributes('-alpha',alpha)
app.wm_attributes('-topmost', 1)

uppath = resource_path("up.png")
photo = PhotoImage(file = uppath)
mpUp = photo.subsample(6, 6)

downpath= resource_path("down.png")
photo = PhotoImage(file = downpath)
mpDown = photo.subsample(6, 6) 


totalpath= resource_path("updown.png")
photo = PhotoImage(file = totalpath)
mpTotal = photo.subsample(24, 24)

closepath= resource_path("close.png")
photo = PhotoImage(file = closepath)
buttonimg = photo.subsample(11, 11)

infopath= resource_path("info.png")
photo = PhotoImage(file = infopath)
infoimg = photo.subsample(14, 14)

iconUp = Label(app ,text = "Up:",background=bgr,foreground='white',font='Helvetica 11 bold',image=mpUp)
iconUp.grid(row = 0,column = 0)
iconDown = Label(app ,text = "Down:",background=bgr,foreground='white',font='Helvetica 11 bold',image=mpDown)
iconDown.grid(row = 1,column = 0)
speedUp = Label(app ,text = "0",background=bgr,foreground='white',font='Helvetica 11 bold')
speedUp.grid(row = 0,column = 1)
speedDown = Label(app ,text = "0",background=bgr,foreground='white',font='Helvetica 11 bold')
speedDown.grid(row = 1,column = 1)

iconTotal = Label(app ,text = "Total:",background=bgr,foreground='white',font='Helvetica 11 bold',image=mpTotal)
iconTotal.grid(row = 2,column = 0)
totalUsage= Label(app ,text = "0",background=bgr,foreground='white',font='Helvetica 11 bold')
totalUsage.grid(row = 2,column = 1)

buttonClose = Button(app, image=buttonimg,background=bgr,borderwidth=0,command =exitNetspeed,state=DISABLED)
buttonClose.place(x=w-28, y=0)
buttonSelectInterface = Button(app, text=interface[0],borderwidth=0,background=bgr,foreground='white',command =getnetinterface,font='Helvetica 10 bold')
buttonSelectInterface.place(x=w-26, y=26)

info = Button(app, image=infoimg,background=bgr,borderwidth=0,command =showInfo)
info.place(x=w-25, y=54)


app.resizable(0, 0)
app.overrideredirect(1)
app.configure(background=bgr)

app.bind("<Enter>", lambda event: buttonClose.config(state=NORMAL))
app.bind("<Leave>", lambda event: buttonClose.config(state=DISABLED))

# to move the window even when dragging is done by clicking the icons
buttonClose.bind("<B1-Motion>", buttonmotion)
speedUp.bind("<B1-Motion>", speedUpmotion)
speedDown.bind("<B1-Motion>", speedDownmotion)
totalUsage.bind("<B1-Motion>", totalUsagemotion)
iconDown.bind("<B1-Motion>", speedDowniconmotion)
iconTotal.bind("<B1-Motion>", totaliconmotion)
buttonSelectInterface.bind("<B1-Motion>", interfacebuttonmotion)
info.bind("<B1-Motion>", infomotion)

app.bind("<Button 1>",getorigin)
app.bind("<B1-Motion>", move_window)
app.bind("<MouseWheel>", scrollmouse)
app.protocol("WM_DELETE_WINDOW", on_closing)



upspeed=(psutil.net_io_counters(pernic=True)[interface].bytes_sent)/1000
downspeed=(psutil.net_io_counters(pernic=True)[interface].bytes_recv)/1000
time.sleep(1)
t = threading.Thread(target=speedCalc, args=(upspeed,downspeed,))
t.daemon = True
t.start()



app.mainloop()


