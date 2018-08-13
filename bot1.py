from Linephu.linepy import *
from Linephu.akad.ttypes import *
import time, random, clock
from time import sleep
import timeit



client = LINE()
client.log("Auth Token : " + str(client.authToken))
#client = LINE('email', 'password')

oepoll = OEPoll(client)

MySelf = client.getProfile()
print("My MID : " + MySelf.mid)

whiteListedMid = ["u52afe1d4ea5332242efacfeb9190d2a3", "u58bc30a989f932d0fd73ccb847107779", "u2a3fb897b9e40c92a5962c43ec178006", "u0fcc0258ddc63ea6feea223e1a571445", "ud417ada62140fb51e46c19ec43b5681b", "ueaff862c8ef0202b937bb2203794ef4a"]


def find_between_r( s, first, last ):
    try:
        start = s.rindex( first ) + len( first )
        end = s.rindex( last, start )
        return s[start:end]
    except ValueError:
        return ""
def lineBot(op):
    try:
        if op.type == 0:
            return
        if op.type ==13:
            print ("[ 13 ] NOTIFIED INVITE INTO GRUUP")
            b = open("b.txt", "r")
            blackListedMid = b.readline()
            b.close()
            if op.param3 in MySelf.mid:
                client.acceptGroupInvitation(op.param1)
            if op.param3 in blackListedMid:
                client.cancelGroupInvitation(op.param1, [op.param3])
            else:
                pass
        if op.type == 19:
            print ("[ 19 ] NOTIFIED KICKOUT FROM GROUP")
            if op.param3 == MySelf.mid:
                hb = open("hb.txt", "r")
                b = open("b.txt", "r")
                halfBlackListedMid = hb.readline()
                blackListedMid = b.readline()
                hb.close()
                b.close()
                if op.param2 not in halfBlackListedMid and op.param3 not in blackListedMid:
                    hb = open("hb.txt", "w")
                    hb.write(op.param2)
                    hb.close()
                elif op.param2 in halfBlackListedMid:
                    b = open("b.txt", "w")
                    b.write(op.param2)
                    b.close()
            else:
                if op.param3 in whiteListedMid:
                    if op.param2 not in whiteListedMid:
                        try:
                            client.kickoutFromGroup(op.param1, [op.param2])
                        except Exception as e:
                            print(e)
                    group = client.getGroup(op.param1)
                    if group.preventedJoinByTicket == True:
                        try:
                            group.preventedJoinByTicket = False
                            str1 = client.reissueGroupTicket(op.param1)
                            client.updateGroup(group)
                            client.sendMessage(op.param3, "/jgurlx gid: " + op.param1 + " gid " + "url: http://line.me/R/ti/g/" + str1 + " url")
                        except Exception as e:
                            print(e)
                    else:
                        try:
                            str1 = client.reissueGroupTicket(op.param1)
                            client.updateGroup(group)
                            client.sendMessage(op.param3, "/jgurlx gid: " + op.param1 + " gid " + "url: http://line.me/R/ti/g/" + str1 + " url")
                        except Exception as e:
                            print(e)
        if op.type == 26:
            print ("[ 26 ] RECRIVE MESSAGE")
            msg = op.message
            try:
                if msg.contentType == 0:
                    try:
                        if msg.toType == 0:
                            print("\n")
                            print("Private Chat Message Received")
                            print("Sender's Name : " + client.getContact(msg._from).displayName)
                            print("Sender's MID : " + msg._from)
                            print("Received Message : " + msg.text)
                            print("\n")
                            if msg._from in whiteListedMid:
                                if msg.text.startswith("/jgurlx"):
                                    str1 = find_between_r(msg.text, "gid: ", " gid")
                                    str2 = find_between_r(msg.text, "url: http://line.me/R/ti/g/", " url")
                                    client.acceptGroupInvitationByTicket(str1, str2)
                                    JoinedGroups.append(str1)
                                    group = client.getGroup(str1)
                                    try:
                                        client.reissueGroupTicket(str1)
                                        group.preventedJoinByTicket = True
                                        client.updateGroup(group)
                                    except Exception as e:
                                        print(e)
                        else:
                            pass
                    except:
                        pass
                else:
                    pass
            except:
                pass
        if op.type == 25:
            print ("[ 25 ] SEND MESSAGE")
            msg = op.message
            if msg.toType == 0:
                if msg.contentType == 0:
                    if msg.text == "speed":
                        start = time.time()
                        elapsed_time = time.time() - start
                        client.sendMessage(msg.to,format(str(elapsed_time)) + "秒")
                    elif msg.text == "mid":
                        client.sendMessage(msg.to, msg.to)
                    elif msg.text == "me":
                        client.sendMessage(msg.to, text=None, contentMetadata={'mid': msg._from}, contentType=13)
                    elif msg.text == "you":
                        client.sendMessage(msg.to, text=None, contentMetadata={'mid': msg.to}, contentType=13)
                else:
                    pass
            if msg.toType == 2:
                if msg.contentType == 0:
                    if msg.text == "invite bot":
                        group = client.getGroup(msg.to)
                        try:
                            group.preventedJoinByTicket = False
                            str1 = client.reissueGroupTicket(msg.to)
                            client.updateGroup(group)
                        except Exception as e:
                            print(e)
                        client.sendMessage("u58bc30a989f932d0fd73ccb847107779", "/jgurl gid: " + msg.to + " gid " + "url: http://line.me/R/ti/g/" + str1 + " url")
                        client.sendMessage("u2a3fb897b9e40c92a5962c43ec178006", "/jgurl gid: " + msg.to + " gid " + "url: http://line.me/R/ti/g/" + str1 + " url")
                        client.sendMessage("u0fcc0258ddc63ea6feea223e1a571445", "/jgurl gid: " + msg.to + " gid " + "url: http://line.me/R/ti/g/" + str1 + " url")
                        client.sendMessage("ud417ada62140fb51e46c19ec43b5681b", "/jgurl gid: " + msg.to + " gid " + "url: http://line.me/R/ti/g/" + str1 + " url")
                        client.sendMessage("ueaff862c8ef0202b937bb2203794ef4a", "/jgurlx gid: " + msg.to + " gid " + "url: http://line.me/R/ti/g/" + str1 + " url")
                    elif msg.text == "speed":
                        start = clock()
                        elapsed_time = clock() - start
                        client.sendMessage(msg.to,format(str(elapsed_time)) + "秒")
                    elif msg.text == "gcreator":
                        group = client.getGroup(msg.to)
                        gc = group.creator.mid
                        client.sendContact(msg.to, gc)
                    elif msg.text == "mid":
                        client.sendMessage(msg.to, msg._from)
                    elif msg.text == "gid":
                        client.sendMessage(msg.to, msg.to)
                    elif msg.text == "ginfo":
                        group = client.getGroup(msg.to)
                        md = "[群組名稱]\n" + group.name + "\n\n[gid]\n" + group.id + "\n\n[群組圖片]\nhttp://dl.profile.line-cdn.net/" + group.pictureStatus
                        if group.preventedJoinByTicket is False: md += "\n\n行動網址: 開啟\n"
                        else: md += "\n\n行動網址: 關閉\n"
                        if group.invitee is None: md += "\n成員數: " + str(len(group.members)) + "人\n\n邀請中: 0人"
                        else: md += "\n成員數: " + str(len(group.members)) + "人\n邀請中: " + str(len(group.invitee)) + "人"
                        client.sendMessage(msg.to, md)
                    elif msg.text == "me":
                        client.sendContact(msg.to, MySelf.mid)
                    elif msg.text == "/destroy":
                        print("start destroying")
                        botlist = ["u2a3fb897b9e40c92a5962c43ec178006", "u0fcc0258ddc63ea6feea223e1a571445", "ud417ada62140fb51e46c19ec43b5681b", "ueaff862c8ef0202b937bb2203794ef4a"]
                        _name = msg.text.replace("/destroy","")
                        group = client.getGroup(msg.to)
                        targets = []
                        for g in group.members:
                            if _name in g.displayName:
                                targets.append(g.mid)
                        if targets == []:
                            client.leaveGroup(msg.to)
                        else:
                            for target in targets:
                                try:
                                    client.sendMessage(random.choice(botlist), "/kick gid: " + msg.to + " gid mid: " + target + " mid")
                                except:
                                    client.sendMessage(msg.to, "錯誤")
                    elif msg.text == "logout":
                        client.sendMessage("u58bc30a989f932d0fd73ccb847107779", "/sm mid: " + msg.to + " mid text: 開始進行登出程序 text")
                        client.sendMessage("u2a3fb897b9e40c92a5962c43ec178006", "/sm mid: " + msg.to + " mid text: 開始進行登出程序 text")
                        client.sendMessage("u0fcc0258ddc63ea6feea223e1a571445", "/sm mid: " + msg.to + " mid text: 開始進行登出程序 text")
                        client.sendMessage("ud417ada62140fb51e46c19ec43b5681b", "/sm mid: " + msg.to + " mid text: 開始進行登出程序 text")
                        client.sendMessage("ueaff862c8ef0202b937bb2203794ef4a", "/sm mid: " + msg.to + " mid text: 開始進行登出程序 text")
                    elif msg.text == "報數":
                        client.sendMessage("u58bc30a989f932d0fd73ccb847107779", "/sm mid: " + msg.to + " mid text: 1 text")
                        time.sleep(0.5)
                        client.sendMessage("u2a3fb897b9e40c92a5962c43ec178006", "/sm mid: " + msg.to + " mid text: 2 text")
                        client.sendMessage("u0fcc0258ddc63ea6feea223e1a571445", "/sm mid: " + msg.to + " mid text: 3 text")
                        client.sendMessage("ud417ada62140fb51e46c19ec43b5681b", "/sm mid: " + msg.to + " mid text: 4 text")
                        client.sendMessage("ueaff862c8ef0202b937bb2203794ef4a", "/sm mid: " + msg.to + " mid text: 5 text")
            else:
                pass
    except Exception as e:
        print(e)

while True:
    try:
        ops = oepoll.singleTrace(count=50)
        if ops is not None:
            for op in ops:
                lineBot(op)
                oepoll.setRevision(op.revision)
    except Exception as e:
        print(e)
