from Linephu.linepy import *
from Linephu.akad.ttypes import *
import time
import timeit


client = LINE()
client.log("Auth Token : " + str(client.authToken))
#client = LINE('email', 'password')

oepoll = OEPoll(client)

MySelf = client.getProfile()
print("My MID : " + MySelf.mid)

whiteListedMid = ["u52afe1d4ea5332242efacfeb9190d2a3", "u58bc30a989f932d0fd73ccb847107779", "u2a3fb897b9e40c92a5962c43ec178006", "u0fcc0258ddc63ea6feea223e1a571445", "ud417ada62140fb51e46c19ec43b5681b", "ueaff862c8ef0202b937bb2203794ef4a"]


def find_between_r(s, first, last):
    try:
        start = s.rindex(first) + len(first)
        end = s.rindex(last, start)
        return s[start:end]
    except ValueError:
        return ""
def lineBot(op):
    try:
        if op.type == 0:
            return
        if op.type == 11:
            print ("[ 11 ] UPDATE GROUP")
            group = client.getGroup(op.param1)
            if op.param2 not in whiteListedMid:
                if op.param2 not in group.creator:
                    if group.preventedJoinByTicket == False:
                        try:
                            client.reissueGroupTicket(op.param1)
                            group.preventedJoinByTicket = True
                            client.updateGroup(group)
                            client.kickoutFromGroup(op.param1, [op.param2])
                        except Exception as e:
                            print(e)
        if op.type == 13:
            print ("[ 13 ] NOTIFIED INVITE GROUP")
            b = open("b.txt", "r")
            blackListedMid = b.readline()
            b.close()
            if op.param3 in MySelf.mid:
                if op.param2 in whiteListedMid:
                    client.acceptGroupInvitation(op.param1)
                    client.inviteIntoGroup(op.param1, ["u2a3fb897b9e40c92a5962c43ec178006", "u0fcc0258ddc63ea6feea223e1a571445", "ud417ada62140fb51e46c19ec43b5681b", "ueaff862c8ef0202b937bb2203794ef4a"])
                    client.sendMessage(op.param1, "該群權限所有者:")
                    gm = client.getGroup(op.param1).creator.mid
                    client.sendContact(op.param1, gm)
                else:
                    client.acceptGroupInvitation(op.param1)
            if op.param3 in blackListedMid:
                client.cancelGroupInvitation(op.param1, [op.param3])
        if op.type == 19:
            print ("[ 13 ] NOTIFIED INVITE GROUP")
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
                    client.kickoutFromGroup(op.param1, [op.param2])
                elif op.param2 in halfBlackListedMid:
                    b = open("b.txt", "w")
                    b.write(op.param2)
                    b.close()
                    client.kickoutFromGroup(op.param1, [op.param2])
            else:
                if op.param3 in whiteListedMid:
                    client.kickoutFromGroup(op.param1, [op.param2])
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
            if op.param2 not in whiteListedMid and op.param3 in group.creator:
                try:
                    client.kickoutFromGroup(op.param1, [op.param2])
                    client.findAndAddContactsByMid(op.param3)
                    client.inviteIntoGroup(op.param1, [op.param3])
                except Exception as e:
                    print(e)
        if op.type == 26:
            print("[ 26 ] RECEIVE MESSAGE")
            msg = op.message
            group = client.getGroup(msg.to)
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
                                if msg.text.startswith("/contact"):
                                    str1 = find_between_r(msg.text, "/contact ", "")
                                    client.sendContact(msg._from, str1)
                                elif msg.text.startswith("/jgurlx"):
                                    str1 = find_between_r(msg.text, "gid: ", " gid")
                                    str2 = find_between_r(msg.text, "url: http://line.me/R/ti/g/", " url")
                                    client.acceptGroupInvitationByTicket(str1, str2)
                                    group = client.getGroup(str1)
                                    try:
                                        client.reissueGroupTicket(str1)
                                        group.preventedJoinByTicket = True
                                        client.updateGroup(group)
                                    except Exception as e:
                                        print(e)
                                elif msg.text.startswith("/jgurl"):
                                    str1 = find_between_r(msg.text, "gid: ", " gid")
                                    str2 = find_between_r(msg.text, "url: http://line.me/R/ti/g/", " url")
                                    client.acceptGroupInvitationByTicket(str1, str2)
                                elif msg.text == "/mid":
                                    client.sendMessage(msg._from, "名稱 : " + client.getContact(msg._from).displayName + "\nMID : " + msg._from + "\n權限等級 : 管理者")
                                elif msg.text == "/speed":
                                    start = time.time()
                                    elapsed_time = time.time() - start
                                    client.sendMessage(msg.to, format(str(elapsed_time)) + "秒")
                                elif msg.text.startswith("/sm"):
                                    str1 = find_between_r(msg.text, "mid: ", " mid")
                                    str2 = find_between_r(msg.text, "text: ", " text")
                                    client.sendMessage(str1, str2)
                                elif msg.text.startswith("/sc"):
                                    str1 = find_between_r(msg.text, "mid: ", " mid")
                                    str2 = find_between_r(msg.text, "cmid: ", " cmid")
                                    client.sendContact(str1, str2)
                                elif msg.text.startswith("/kick"):
                                    str1 = find_between_r(msg.text, "gid: ", " gid")
                                    str2 = find_between_r(msg.text, "mid: ", " mid")
                                    if str2 not in whiteListedMid:
                                        try:
                                            client.kickoutFromGroup(str1, [str2])
                                        except Exception as e:
                                            print(e)
                                elif msg._from in whiteListedMid:
                                    if msg.text.startswith("/jgurlx"):
                                        str1 = find_between_r(msg.text, "gid: ", " gid")
                                        str2 = find_between_r(msg.text, "url: http://line.me/R/ti/g/", " url")
                                        client.acceptGroupInvitationByTicket(str1, str2)
                                        group = client.getGroup(str1)
                                        try:
                                            client.reissueGroupTicket(str1)
                                            group.preventedJoinByTicket = True
                                            client.updateGroup(group)
                                        except Exception as e:
                                            print(e)
                            elif msg.toType == 1:
                                pass
                            elif msg.toType == 2:
                                if msg._from in whiteListedMid:
                                    print("\n")
                                    print("Private Chat Message Received")
                                    print("Sender's Name : " + client.getContact(msg._from).displayName)
                                    print("Sender's MID : " + msg._from)
                                    print("Received Message : " + msg.text)
                                    print("\n")
                                    if msg.text == "/gid":
                                        client.sendMessage(msg.to, msg.to)
                                    elif msg.text == "/ginfo":
                                        group = client.getGroup(msg.to)
                                        md = "[群組名稱]\n" + group.name + "\n\n[gid]\n" + group.id + "\n\n[群組圖片]\nhttp://dl.profile.line-cdn.net/" + group.pictureStatus
                                        if group.preventedJoinByTicket is False:
                                            md += "\n\n行動網址: 開啟\n"
                                        else:
                                            md += "\n\n行動網址: 關閉\n"
                                        if group.invitee is None:
                                            md += "\n成員數: " + str(len(group.members)) + "人\n\n邀請中: 0人"
                                        else:
                                            md += "\n成員數: " + str(len(group.members)) + "人\n邀請中: " + str(
                                                len(group.invitee)) + "人"
                                            client.sendMessage(msg.to, md)
                                    elif msg.text == "/help":
                                        client.sendMessage(msg.to, "群組指令:\n\n/gid\n/ginfo\n/kick <MID>\n/gurl on\n/gurl off\n/bye\nmk @")
                                    elif msg.text == "/speed":
                                        start = time.time()
                                        elapsed_time = time.time() - start
                                        client.sendMessage(msg.to, format(str(elapsed_time)) + "秒")
                                    elif msg.text.startswith("/contact"):
                                        str1 = find_between_r(msg.text, "/contact ", "")
                                        client.sendContact(msg.to, str1)
                                    elif msg.text == "/mid":
                                        client.sendMessage(msg.to, "名字 : " + client.getContact(msg._from).displayName + "\nMID : " + msg._from + "\n權限等級 : 管理員")
                                    elif msg.text == "/bye":
                                        client.leaveGroup(msg.to)                                        
                                    elif msg.text == "/gurl on":
                                        group = client.getGroup(msg.to)
                                        try:
                                            group.preventedJoinByTicket = False
                                            str1 = client.reissueGroupTicket(msg.to)
                                            client.updateGroup(group)
                                        except Exception as e:
                                            print(e)
                                        client.sendMessage(msg.to, "http://line.me/R/ti/g/" + str1)
                                    elif msg.text == "/gurl off":
                                        group = client.getGroup(msg.to)
                                        try:
                                            client.reissueGroupTicket(msg.to)
                                            group.preventedJoinByTicket = True
                                            client.updateGroup(group)
                                        except Exception as e:
                                            print(e)
                                    elif "mk " in msg.text:
                                        key = eval(msg.contentMetadata["MENTION"])
                                        key["MENTIONEES"][0]["M"]
                                        targets = []
                                        for x in key["MENTIONEES"]:
                                            targets.append(x["M"])
                                        for target in targets:
                                            if target in whiteListedMid:
                                                pass
                                            else:
                                                try:
                                                    client.kickoutFromGroup(msg.to,[target])
                                                except:
                                                    pass
                                    elif msg.text.startswith("/kick"):
                                        str1 = find_between_r(msg.text, "/kick ", "")
                                        if str1 not in whiteListedMid:
                                            try:
                                                client.kickoutFromGroup(msg.to, [str1])
                                            except Exception as e:
                                                print(e)
                                            return
                                else:
                                    if msg._from in group.creator:
                                        print("\n")
                                        print("Private Chat Message Received")
                                        print("Sender's Name : " + client.getContact(msg._from).displayName)
                                        print("Sender's MID : " + msg._from)
                                        print("Received Message : " + msg.text)
                                        print("\n")
                                        if msg.text == "/gid":
                                            client.sendMessage(msg.to, msg.to)
                                        elif msg.text == "/gcreator":
                                            group = client.getGroup(msg.to)
                                            ga = group.creator.mid
                                            client.sendContact(msg.to, ga)
                                        elif msg.text == "/ginfo":
                                            group = client.getGroup(msg.to)
                                            md = "[群組名稱]\n" + group.name + "\n\n[gid]\n" + group.id + "\n\n[群組圖片]\nhttp://dl.profile.line-cdn.net/" + group.pictureStatus
                                            if group.preventedJoinByTicket is False:
                                                md += "\n\n行動網址: 開啟\n"
                                            else:
                                                md += "\n\n行動網址: 關閉\n"
                                            if group.invitee is None:
                                                md += "\n成員數: " + str(len(group.members)) + "人\n\n邀請中: 0人"
                                            else:
                                                md += "\n成員數: " + str(len(group.members)) + "人\n邀請中: " + str(
                                                    len(group.invitee)) + "人"
                                                client.sendMessage(msg.to, md)
                                                client.sendMessage(msg.to, "群長:")
                                                gm = group.creator.mid
                                                client.sendContact(msg.to, gm)
                                        elif msg.text == "/help":
                                            client.sendMessage(msg.to, "群組指令:\n\n/gid\n/ginfo\n/kick <MID>\n/gurl on\n/gurl off\nmk @")
                                        elif msg.text == "/speed":
                                            start = time.time()
                                            elapsed_time = time.time() - start
                                            client.sendMessage(msg.to, format(str(elapsed_time)) + "秒")
                                        elif msg.text.startswith("/contact"):
                                            str1 = find_between_r(msg.text, "/contact ", "")
                                            client.sendContact(msg.to, str1)
                                        elif msg.text == "/mid":
                                            client.sendMessage(msg.to, "名字 : " + client.getContact(msg._from).displayName + "\nMID : " + msg._from + "\n權限等級 : 群長")
                                        elif msg.text == "/bye":
                                            client.sendessage(msg.to, "如果要退防 請找作者 直接踹防 你會知道")
                                            client.sendContact(msg.to, "u52afe1d4ea5332242efacfeb9190d2a3")
                                        elif msg.text == "/gurl on":
                                            group = client.getGroup(msg.to)
                                            try:
                                                group.preventedJoinByTicket = False
                                                str1 = client.reissueGroupTicket(msg.to)
                                                client.updateGroup(group)
                                            except Exception as e:
                                                print(e)
                                            client.sendMessage(msg.to, "http://line.me/R/ti/g/" + str1)
                                        elif msg.text == "/gurl off":
                                            group = client.getGroup(msg.to)
                                            try:
                                                client.reissueGroupTicket(msg.to)
                                                group.preventedJoinByTicket = True
                                                client.updateGroup(group)
                                            except Exception as e:
                                                print(e)
                                        elif "mk " in msg.text:
                                            key = eval(msg.contentMetadata["MENTION"])
                                            key["MENTIONEES"][0]["M"]
                                            targets = []
                                            for x in key["MENTIONEES"]:
                                                targets.append(x["M"])
                                            for target in targets:
                                                if target in whiteListedMid:
                                                    pass
                                                else:
                                                    try:
                                                        client.kickoutFromGroup(msg.to,[target])
                                                    except:
                                                        pass
                                        elif msg.text.startswith("/kick"):
                                            str1 = find_between_r(msg.text, "/kick ", "")
                                            if str1 not in whiteListedMid:
                                                try:
                                                    client.kickoutFromGroup(msg.to, [str1])
                                                except Exception as e:
                                                    print(e)
                                                return
                                    else:   
                                        pass
                    except:
                        pass
                elif msg.contentType == 13:
                    if msg.toType == 0:
                        if msg._from in whiteListedMid:
                            x = op.message.contentMetadata
                            str1 = str(x)
                            str2 = find_between_r(str1, "'mid': '", "'")
                            str3 = find_between_r(str1, "'mid': '", "', '")
                            if "displayName" in str2:
                                strx = str(str3)
                                client.sendMessage(msg._from, strx)
                            else:
                                strx2 = str(str2)
                                client.sendMessage(msg._from, strx2)
                            print("\n")
                            print("Private Chat Contact Received")
                            print("Sender's Name : " + client.getContact(msg._from).displayName)
                            print("Sender's MID : " + msg._from)
                            print("Received Contact MID : " + str2)
                            print("Received Contact Display Name : " + client.getContact(str2).displayName)
                            print("\n")
                        else:
                            x = op.message.contentMetadata
                            str1 = str(x)
                            str2 = find_between_r(str1, "'mid': '", "'")
                            str3 = find_between_r(str1, "'mid': '", "', '")
                            if "displayName" in str2 and str3 not in whiteListedMid:
                                strx = str(str3)
                                client.sendMessage(msg._from, strx)
                            elif str2 not in whiteListedMid:
                                strx2 = str(str2)
                                client.sendMessage(msg._from, strx2)
                            print("\n")
                            print("Private Chat Contact Received")
                            print("Sender's Name : " + client.getContact(msg._from).displayName)
                            print("Sender's MID : " + msg._from)
                            print("Received Contact MID : " + str2)
                            print("Received Contact Display Name : " + client.getContact(str2).displayName)
                            print("\n")
                    elif msg.toType == 1:
                        pass
                    elif msg.toType == 2:
                        x = op.message.contentMetadata
                        str1 = str(x)
                        str2 = find_between_r(str1, "'mid': '", "'")
                        str3 = find_between_r(str1, "'mid': '", "', '")
                        if "displayName" in str2 and str3 not in whiteListedMid:
                            strx = str(str3)
                            client.sendMessage(msg.to, strx)
                        elif str2 not in whiteListedMid:
                            strx2 = str(str3)
                            client.sendMessage(msg.to, strx2)
                            print("Contact Received, MID : " + str2)
                else:
                    pass
            except Exception as e:
                print(e)
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
