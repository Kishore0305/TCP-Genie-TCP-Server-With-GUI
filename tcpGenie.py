from tkinter import mainloop,Label,Button,Tk,Entry
import socket
import subprocess
import threading
gPort=8000
class initiateTCP:
    global gPort
    port = gPort
    listen_queue = 5
    def __init__(self,port,queue):
        initiateTCP.serverSocketObject = socket.socket()
        initiateTCP.serverSocketObject.settimeout(10)
        initiateTCP.port = port
        initiateTCP.listen_queue = queue
        initiateTCP.serverSocketObject.bind(("", initiateTCP.port))
        initiateTCP.serverSocketObject.listen(initiateTCP.listen_queue)

    def wLan_IP():
        result = subprocess.run('ipconfig', stdout=subprocess.PIPE, text=True).stdout.lower()
        scan = 0
        for i in result.split('\n'):
            if 'wireless' in i: scan = 1
            if scan:
                if 'ipv4' in i: return i.split(':')[1].strip()
class clientConnect:
    def __init__(self):
        pass
    def connect(self,tcpObject):
        try:
            self.clientSocket,self.clientAddr=tcpObject.serverSocketObject.accept()
        except:
            return "Timeout"
    def clientDisconnect(self):
        self.clientSocket.close()
    def dataSend(self,data="Terminate"):
        return self.clientSocket.send(data.encode())
    def dataReceived(self):
        try:
            msg=self.clientSocket.recv(1024)
        except socket.error:
            return "Terminate"
        else:
            return msg.decode()
        return self.clientSocket.recv(1024).decode()
def changePort():
    global gPort
    gPort=int(portEntry.get())
def connectClient():
    def helper():
        global gPort
        tcp = initiateTCP(gPort, 5)

        portButton.configure(state="disabled")
        portEntry.configure(state="disabled")
        receivedMessage.configure(text="None")
        connectButton.configure(text="Connecting....",state="disabled")

        client=clientConnect()
        clientResp=client.connect(tcp)
        if clientResp == "Timeout":
            connectButton.configure(text="Connect", command=connectClient,state="normal")
            portButton.configure(state="normal")
            portEntry.configure(state='normal')
            receivedMessage.configure(text="Connection Timed Out")
            return
        clientlabel.configure(text=str(client.clientAddr[0]))
        connectButton.configure(text="Disconnect",command=client.clientDisconnect,state="normal")
        data=None
        while True:
            data=client.dataReceived()
            if not data or data=="Terminate":
                break
            else:
                receivedMessage.configure(text=data[:15])
        client.clientSocket.close()
        tcp.serverSocketObject.close()

        connectButton.configure(text="Connect",command=connectClient)
        portButton.configure(state="normal")
        portEntry.configure(state='normal')
        clientlabel.configure(text="None")
        receivedMessage.configure(text="None")

    clientThread=threading.Thread(target=helper)
    clientThread.daemon=True
    clientThread.start()



root=Tk()
root.title("TCPGenie")
root.geometry("350x190")
root.resizable(False,False)
try:
    root.iconbitmap("genie.ico")
except:
    pass

Label(root,text="Host IP      : ").grid(row=0,column=0,padx=25,pady=10)
hostlabel=Label(root,text=f"{initiateTCP.wLan_IP()} ")
hostlabel.grid(row=0,column=1,padx=25,pady=10)

portButton=Button(root,text="Change Port",command=changePort)
portButton.grid(row=1,column=0)
portEntry=Entry(root)
portEntry.grid(row=1,column=1,padx=25,pady=10)
portEntry.insert(0,str(gPort))

Label(root,text="Client IP      : ").grid(row=2,column=0,padx=25,pady=10)
clientlabel=Label(root,text=f"None")
clientlabel.grid(row=2,column=1,padx=25,pady=10)

connectButton = Button(root,text="Connect",command =connectClient)
connectButton.grid(row=3,column=0)
receivedMessage = Label(root,text="None")
receivedMessage.grid(row=3,column=1)


root.mainloop()

