#from cgitb import text
from asyncio.windows_events import NULL
from concurrent.futures import thread
from sqlite3 import Timestamp
#from curses import baudrate
from tkinter import*
import tkinter as tk
import json
from tkinter.font import BOLD
import requests
import datetime
import serial
import os
import io
import binascii
import sys
import codecs
from PIL import Image
from smartcard.System import readers
from smartcard.util import HexListToBinString, toHexString, toBytes
import threading
import time
import socket
import urllib.request as request
import json
import playsound
import pygame

import hl7
from hl7.client import MLLPClient
pygame.init()
#pygame.mixer.init()
root = Tk()
root.title("Demo Smart OPD")
# root.iconbitmap('/path/to/ico/icon.ico') # icon
root.geometry("800x1280")
root.attributes('-fullscreen',True) #Fullscreen
bgimg= tk.PhotoImage(file = "C:\\Users\\X8pro\\Documents\\acemed bp\\ACE-MED_beta\\image.png")
bgSettingImg= tk.PhotoImage(file = "C:\\Users\X8pro\\Documents\\acemed bp\\ACE-MED_beta\\setting.png")
limg= Label(root, i=bgimg).pack()
isHn=False

strHn=tk.StringVar(root)
tName=tk.StringVar(root)
tGender=tk.StringVar(root)
tBirth=tk.StringVar(root)
tAge=tk.StringVar(root)
tTemp=tk.StringVar(root)
tSys=tk.StringVar(root)
tDia=tk.StringVar(root)
tPul=tk.StringVar(root)
tWeight=tk.StringVar(root)
tHeight=tk.StringVar(root)
tBmi=tk.StringVar(root)
#Label_ID = Label(textvariable=tHn,fg="black",font=300,bg ="white").place(x=90,y=72)
Label_Name = Label(textvariable=tName,fg="blue",font=("Arial Black", 25),bg ="white").place(x=161,y=133,height=48)
Label_Gender = Label(textvariable=tGender,fg="blue",font=("Arial Black", 25),bg ="white").place(x=161,y=204,height=48)
Label_Age = Label(textvariable=tBirth,fg="blue",font=("Arial Black", 25),bg ="white").place(x=197,y=274)
Label_AgeSum = Label(textvariable=tAge,fg="blue",font=("Arial Black", 25),bg ="white").place(x=660,y=275)

Label_Temp = Label(textvariable=tTemp,justify='center',fg="blue",font=("Arial Black", 50),bg ="white").place(x=476,y=394,width= 152,height=112)
Label_SYS = Label(root,textvariable=tSys,justify='center',fg="blue",font=("Arial Black", 50),bg ="white")
Label_SYS.place(x=390,y=600,width= 182,height=83)
Label_DIA = Label(root,textvariable=tDia,justify='center',fg="blue",font=("Arial Black", 50),bg ="white")
Label_DIA.place(x=390,y=729,width= 182,height=83)
Label_Pulse = Label(root,textvariable=tPul,justify='center',fg="blue",font=("Arial Black", 50),bg ="white")
Label_Pulse.place(x=390,y=857,width= 182,height=83)
Label_Height = Label(textvariable=tHeight,justify='center',fg="blue",font=("Arial Black", 20),bg ="white").place(x=400,y=997)
Label_Weight = Label(textvariable=tWeight,justify='center',fg="blue",font=("Arial Black", 20),bg ="white").place(x=400,y=1051)
Label(textvariable=tBmi,justify='center',fg="blue",font=("Arial Black", 20),bg ="white").place(x=400,y=1105)
isCid=True
mTemp=False
mBp=False
mWeight=False
isKeypad=False

def play(f):
    pygame.mixer.music.load(f) #Loading File Into Mixer
    pygame.mixer.music.rewind()
    pygame.mixer.music.play() #Playing It In The Whole Device

def clearData():
    global againFlag, isHn
    isHn=False
    againFlag=0
    tName.set('')
    tGender.set('')
    tBirth.set('')
    tAge.set('')
    tTemp.set('')
    tSys.set('')
    tDia.set('')
    tPul.set('')
    tWeight.set('')
    tHeight.set('')
    tBmi.set('')
    strHn.set('')

def calAge(birthDate):
    td=datetime.datetime.today()
    iYear=int(birthDate[:4])-543
    iMon=int(birthDate[4:6])
    iDay=int(birthDate[6:])
    bd=datetime.date(iYear,iMon,iDay)
    age=td.year-iYear-((td.month,td.day)<(iMon,iDay))
    return age

def readSmartCart():    
    global againFlag,isCid,isHn
# Thailand ID Smartcard
    def thai2unicode(data):
        result = ''
        result = bytes(data).decode('tis-620')
        return result.strip();
    def getData(cmd, req = [0x00, 0xc0, 0x00, 0x00]):
        data, sw1, sw2 = connection.transmit(cmd)
        data, sw1, sw2 = connection.transmit(req + [cmd[-1]])
        return [data, sw1, sw2];
    # Check card
    SELECT = [0x00, 0xA4, 0x04, 0x00, 0x08]
    THAI_CARD = [0xA0, 0x00, 0x00, 0x00, 0x54, 0x48, 0x00, 0x01]
    # CID
    CMD_CID = [0x80, 0xb0, 0x00, 0x04, 0x02, 0x00, 0x0d]
    # TH Fullname
    CMD_THFULLNAME = [0x80, 0xb0, 0x00, 0x11, 0x02, 0x00, 0x64]
    # EN Fullname
    CMD_ENFULLNAME = [0x80, 0xb0, 0x00, 0x75, 0x02, 0x00, 0x64]
    # Date of birth
    CMD_BIRTH = [0x80, 0xb0, 0x00, 0xD9, 0x02, 0x00, 0x08]
    # Gender
    CMD_GENDER = [0x80, 0xb0, 0x00, 0xE1, 0x02, 0x00, 0x01]
    # Get all the available readers
    readerList = readers()
    #print ('Available readers:')
    #for readerIndex,readerItem in enumerate(readerList):
    #    print(readerIndex, readerItem)
    # Select reader
    readerSelectIndex = 0 #int(input("Select reader[0]: ") or "0")
    reader = readerList[readerSelectIndex]
    connection = reader.createConnection()
    connection.connect()
    atr = connection.getATR()
    if (atr[0] == 0x3B & atr[1] == 0x67):
        req = [0x00, 0xc0, 0x00, 0x01]
    else :
        req = [0x00, 0xc0, 0x00, 0x00]
    # Check card
    data, sw1, sw2 = connection.transmit(SELECT + THAI_CARD)
    # CID
    data = getData(CMD_CID, req)
    cid = thai2unicode(data[0])
    strHn.set(cid)
    # TH Fullname
    data = getData(CMD_THFULLNAME, req)
    strFname=thai2unicode(data[0])
    strFnameS1=strFname.split('##')
    strFnameS2=strFnameS1[0].split('#')
    name=strFnameS2[0]+strFnameS2[1]+' '+strFnameS1[1]
    tName.set(name)
    #print(thai2unicode2(data[0])))
    # EN Fullname
    #data = getData(CMD_ENFULLNAME, req)
    #print ("EN Fullname: " + thai2unicode(data[0]))    
    # Date of birth
    data = getData(CMD_BIRTH, req)
    temp=thai2unicode(data[0])
    print(temp)
    tBirth.set(temp)
    age=calAge(temp)
    tAge.set(age)    
    # Gender
    data = getData(CMD_GENDER, req)
    print(data)
    if(thai2unicode(data[0])=='1'):
        tGender.set('ชาย')
    else:
        tGender.set('หญิง')
    againFlag=0
    isCid=True
    isHn=True

def thrScardCallback():
    while True:
        try:
            readSmartCart()
            break
        except:
            time.sleep(1)

def settingBtnCallback(event):
    #setting page
    global thrBpFlag,thrWeightFlag
    def save(event):
        with open('config.txt','w') as f:
            str=strIpDev.get()+','+strSnDev.get()+','+strLocDev.get()+','+strWeb.get() \
                +','+strIpSer.get()+','+strPortSer.get()+','+strBpPort.get()+','+strTempPort.get() \
                    +','+strWeigthPort.get()
            f.write(str)
            settingWindow.destroy()
            thrBpFlag=True
            thrWeightFlag=True
            thrBp=threading.Thread(target=getBp)
            thrBp.setDaemon(True)
            thrBp.start()
            thrWeight=threading.Thread(target=getWeight)
            thrWeight.setDaemon(True)
            thrWeight.start()
            thrScard=threading.Thread(target=thrScardCallback)
            thrScard.setDaemon(True)
            thrScard.start()
            thrTemp=threading.Thread(target=getTemp)
            thrTemp.setDaemon(True)
            thrTemp.start()
    settingWindow = Toplevel(root)
    settingWindow.geometry('800x1280')    
    settingWindow.attributes('-fullscreen',True) #Fullscreen
    bl=Label(settingWindow,i=bgSettingImg).place(x=0,y=0)

    strIpDev=tk.StringVar(settingWindow)
    strSnDev=tk.StringVar(settingWindow)
    strLocDev=tk.StringVar(settingWindow)
    strWeb=tk.StringVar(settingWindow)
    strIpSer=tk.StringVar(settingWindow)
    strPortSer=tk.StringVar(settingWindow)
    strBpPort=tk.StringVar(settingWindow)
    strTempPort=tk.StringVar(settingWindow)
    strWeigthPort=tk.StringVar(settingWindow)
    f=open('config.txt','r')
    str=f.read()
    f.close()
    strSp=str.split(',')
    strIpDev.set(strSp[0])
    strSnDev.set(strSp[1])
    strLocDev.set(strSp[2])
    strWeb.set(strSp[3])
    strIpSer.set(strSp[4])
    strPortSer.set(strSp[5])
    strBpPort.set(strSp[6])
    strTempPort.set(strSp[7])
    strWeigthPort.set(strSp[8])
    Entry(settingWindow,font=('Arial Black',20),textvariable=strIpDev).place(x=290,y=192,width=485,height=63)
    Entry(settingWindow,font=('Arial Black',20),textvariable=strSnDev).place(x=147,y=260,width=628,height=63)
    Entry(settingWindow,font=('Arial Black',20),textvariable=strLocDev).place(x=248,y=328,width=527,height=63)
    Entry(settingWindow,font=('Arial Black',20),textvariable=strWeb).place(x=32,y=502,width=741,height=63)
    Entry(settingWindow,font=('Arial Black',20),textvariable=strIpSer).place(x=290,y=687,width=485,height=63)
    Entry(settingWindow,font=('Arial Black',20),textvariable=strPortSer).place(x=165,y=755,width=610,height=63)
    Entry(settingWindow,font=('Arial Black',20),textvariable=strBpPort).place(x=201,y=943,width=574,height=63)
    Entry(settingWindow,font=('Arial Black',20),textvariable=strTempPort).place(x=201,y=1011,width=574,height=63)
    Entry(settingWindow,font=('Arial Black',20),textvariable=strWeigthPort).place(x=329,y=1079,width=446,height=63)
    btnSave=Button(settingWindow,text='SAVE',font=("Arial Black", 25),bg = "#8AC185",borderwidth=0)    
    btnSave.bind('<Button>',save)
    btnSave.place(x=350,y=1190)
    #btnSave.pack(side=BOTTOM)
    
def getHn(event):
    global strHn,tName,tGender,tBirth,isCid,isHn,mWeight,mTemp,mBp,againFlag
    #url='https://smartipd-demo-api-z3cqsurxaq-de.a.run.app/patient/1'    
    f=open('config.txt','r')
    tmp = f.read().split(',')
    f.close()
    url=tmp[3]+strHn.get()   
    with request.urlopen(url) as url:
        data=json.load(url)
        tName.set(data['prename']+data['firstname']+' '+data['lastname'])
        if(data['getnder']=='Female'):
            tGender.set('หญิง')
        else:
            tGender.set('ชาย')
        tmp=data['birthdate']
        tBirth.set(tmp)
        iy=int(tmp[:4])+543
        tmp=str(iy)+tmp[5:7]+tmp[8:]
        age=calAge(tmp)
        tAge.set(age)    
        isCid=False
        isHn=True
        print(data)
        if(mWeight and mTemp and mBp and isHn and againFlag):
            hl7Sent()

def getTemp():
    global thrTempFlag,mTemp,mWeight,mBp,isHn,againFlag
    thrTempFlag=False
    f=open('config.txt','r')
    tmp = f.read().split(',')
    f.close()
    ser=serial.Serial()
    ser.port=tmp[7]
    ser.open()
    str1=b'' 
    print(type(str1))    
    if(ser.isOpen):
        print('go')
    while True:
        c=ser.read()
        print(c)
        if(c==b'C'):
            print(str1)
            dStr=str1.decode()    
            str1=b''        
            print(dStr)
            strSp=dStr.split(':')      
            tTemp.set(strSp[1])      
            fTemp=float(strSp[1])
            if(fTemp>37.5):
                play('C:\\Users\\X8pro\\Documents\\acemed bp\\ACE-MED_beta\\tempHigh.wav')
            else:
                play('C:\\Users\\X8pro\\Documents\\acemed bp\\ACE-MED_beta\\tempNormal.wav')
            #ser.close()
            #thrWeightFlag=True
            mTemp=True
            if(mWeight and mTemp and mBp and isHn and againFlag==0):
                hl7Sent()
        else:
            str1+=c
        if(thrTempFlag):
            ser.close()
            break

def hl7Sent():
    global strHn,tTemp,tSys,tDia,tPul,tWeight,tHeight,tBmi,isCid,mTemp,mBp,mWeight,thrScard  
    f=open('config.txt','r')
    tmp = f.read().split(',')
    f.close()
    dt = datetime.datetime.now()
    ts = datetime.datetime.timestamp(dt)
    date_time = datetime.datetime.fromtimestamp(ts)
    timeStamp=date_time.strftime("%Y%m%d%H%M%S")
    strMsg = "MSH|^~\\&|" + tmp[1] + "|"+tmp[2]+"|HIS|BMS-HOSxP|" + timeStamp + "||ORU^R01|2701|P|2.3\n";
    if(isCid):        
        strMsg += "PID|||" + strHn.get() + "\n";
    else:
        strMsg += "PID||" + strHn.get() + "\n";
    strMsg += "PV1||O|||||||||||||||||\n";
    strMsg += "OBR|1||||" + timeStamp + "||||||||" + timeStamp + "\n";
    strMsg += "OBX|1|ST|WEIGHT||" + tWeight.get() + "|Kg|||||F|||" + timeStamp + "\n";
    strMsg += "OBX|2|ST|HEIGHT||" + tHeight.get() + "|cm|||||F|||" + timeStamp + "\n";
    strMsg += "OBX|3|ST|BMI||" + tBmi.get() + "|Kg/m2|||||F|||" + timeStamp + "\n";
    strMsg += "OBX|4|ST|TEMP||" + tTemp.get() + "|C|||||F|||" + timeStamp + "\n";
    strMsg += "OBX|5|ST|SYSTOLIC||" + tSys.get() + "|mmHg|||||F|||" + timeStamp + "\n";
    strMsg += "OBX|6|ST|DIASTOLIC||" + tDia.get() + "|mmHg|||||F|||" + timeStamp + "\n";
    strMsg += "OBX|7|ST|PULSE||" + tPul.get() + "|bpm|||||F|||" + timeStamp + "\n";
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((tmp[4], int(tmp[5])))
            s.sendall(strMsg.encode())
            mTemp=False
            mBp=False
            mWeight=False
            clearData()     
    except:
        pass  

def getBp():
    global thrBpFlag, againFlag,mBp,mTemp,mWeight,isHn
    thrBpFlag=False
    againFlag=0
    f=open('config.txt','r')
    tmp = f.read().split(',')
    f.close()
    ser=serial.Serial()
    ser.port=tmp[6]
    ser.baudrate=2400
    ser.open()
    if(ser.isOpen):
        print('go')
    while True:
        try:
            str1=ser.readline()
            dStr=str1.decode()
            print(type(dStr))
            str2=dStr.split(',')
            if(len(str2)>=11):
                iSys=int(str2[7])
                iDia=int(str2[8])
                iPul=int(str2[9])
                tSys.set(iSys)
                tDia.set(iDia)
                tPul.set(iPul)
                if(iSys>180 or iDia>110):
                    Label_SYS.config(fg='red') 
                    againFlag+=1
                    print(againFlag)
                    print(isHn)
                    if(againFlag<3):
                        print('High1')
                        play("C:\\Users\\X8pro\\Documents\\acemed bp\\ACE-MED_beta\\Pressure_Again.wav")    
                    else:
                        print('hihg2')
                        play("C:\\Users\\X8pro\\Documents\\acemed bp\\ACE-MED_beta\\Pressure_High.wav")    
                        
                elif(iSys>160 or iDia>100):
                    Label_SYS.config(fg='orange')
                    againFlag+=1
                    if(againFlag<3):             
                        play("C:\\Users\\X8pro\\Documents\\acemed bp\\ACE-MED_beta\\Pressure_Again.wav")
                elif(iSys>140 or iDia>90):
                    Label_SYS.config(fg='orange')
                    againFlag+=1
                    if(againFlag<3):         
                        play("C:\\Users\\X8pro\\Documents\\acemed bp\\ACE-MED_beta\\Pressure_Again.wav")         
                else:
                    Label_SYS.config(fg='blue')
                mBp=True
                if(mBp and againFlag==0 and isHn):
                    hl7Sent()
                if(againFlag>=3):
                    print('send high')
                    hl7Sent()
                #ser.close()
                #thrBpFlag=True
            if(thrBpFlag):
                ser.close()
                break
        except:
            pass
def getWeight():
    global thrWeightFlag,mWeight,mTemp,mBp,isHn,againFlag
    thrWeightFlag=False
    f=open('config.txt','r')
    tmp = f.read().split(',')
    f.close()
    ser=serial.Serial()
    ser.port=tmp[8]
    ser.open()
    str1=b''  
    while True:
        c=ser.read()
        str1+=c
        if(c==b'\x03'):
            ddStr=str1.decode()    
            str1=b''     
            sStr=ddStr.split('@')
            dStr=sStr[1]
            print(dStr)
            print(len(dStr))
            tmp1=dStr[0:3]
            tmp2=dStr[3:5]
            tmp3=dStr[6:9]
            tmp4=dStr[9:11]
            tmp5=dStr[37:39]
            tmp7=dStr[39:40]
            fHeight=float(tmp3+'.'+tmp4)
            fWeight=float(tmp1+'.'+tmp2)
            fBmi=float(tmp5+'.'+tmp7)
            tWeight.set("{:.2f}".format(fWeight))
            tHeight.set(fHeight)
            tBmi.set(fBmi)
            mWeight=True
            if(mWeight and mTemp and mBp and isHn and againFlag==0):
                hl7Sent()
            #ser.close()
            #thrWeightFlag=True
        if(thrWeightFlag):
            ser.close()
            break
def btnClearCallback(event):
    global thrScard
    clearData()    
    print(thrScard)
    if(thrScard==NULL):
        thrScard=threading.Thread(target=thrScardCallback)
        thrScard.setDaemon(True)
        thrScard.start()
def btnSaveCallback(event):
    hl7Sent()

def keyPadCallback(event):
    global strHn,varT,isKeypad
    
    def code(value):
        global e,isKeypad
        print(value)
        if(value=='En'):
            isKeypad=False
            getHn(event)
            rootKp.destroy()
        elif(value=='C'):
            strHn.set('')
            isKeypad=False
            rootKp.destroy()
        else:
            t= strHn.get()
            strHn.set(t+value)

    # --- main ---

    keys = [
        ['1', '2', '3'],    
        ['4', '5', '6'],    
        ['7', '8', '9'],    
        ['C', '0', 'En'],    
    ]
    if(isKeypad==False):
        rootKp = Toplevel(root)
        rootKp.geometry('350x510+200+200') 
        isKeypad=True
        rootKp.overrideredirect(True)
        # place to display pin
        varT=tk.StringVar(rootKp)
        #et = tk.Entry(rootKp,textvariable=varT)
        #et.grid(row=0, column=0, columnspan=13, ipady=5)
        # create buttons using `keys`
        for y, row in enumerate(keys, 0):
            for x, key in enumerate(row):
                # `lambda` inside `for` has to use `val=key:code(val)` 
                # instead of direct `code(key)`
                b = tk.Button(rootKp, text=key, command=lambda val=key:code(val))
                b.grid(row=y, column=x, ipadx=50, ipady=50)


thrBp=threading.Thread(target=getBp)
thrBp.setDaemon(True)
thrBp.start()
thrWeight=threading.Thread(target=getWeight)
thrWeight.setDaemon(True)
thrWeight.start()
thrScard=threading.Thread(target=thrScardCallback)
thrScard.setDaemon(True)
thrScard.start()
thrTemp=threading.Thread(target=getTemp)
thrTemp.setDaemon(True)
thrTemp.start()
thrBpFlag=False
thrWeightFlag=False

#Edit text hn
eHn = Entry(root,textvariable=strHn,fg="blue",font=("Arial Black", 20),borderwidth=0)
eHn.bind('<Key-Return>',getHn)
eHn.place(x=323,y=34,width=339,height=66)
eHn.focus()
#Button setting 
bgSettingIcon=PhotoImage(file=r'settingIcon.png')
settingBtn = Button(root,image=bgSettingIcon,bg = "#8AC185",borderwidth=0)
settingBtn.bind('<Button>',settingBtnCallback)
settingBtn.place(x=600,y=1185)

#Button start 
bgEraser=PhotoImage(file=r'eraser.png')
btnStart = Button(root,image=bgEraser,bg = "#8AC185",borderwidth=0)
btnStart.bind('<Button>',btnClearCallback)
btnStart.place(x=115,y=1185)

#Button save 
bgSAVE=PhotoImage(file=r'diskette.png')
btnSAVE = Button(root,image=bgSAVE,bg = "#8AC185",borderwidth=0)
btnSAVE.bind('<Button>',btnSaveCallback)
btnSAVE.place(x=350,y=1185)

#Button save 
bg1=PhotoImage(file=r'keyboard.png')
btnKey = Button(root,image=bg1,bg="#FFFFFF",borderwidth=0)
btnKey.bind('<Button>',keyPadCallback)
btnKey.place(x=670,y=32)
root.mainloop()