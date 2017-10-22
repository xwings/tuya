Team: CLGT

Title: Dr. Bob


Description as below

```
There are elections at the moment for the representative of the students and the
winner will be announced tomorrow by the head of elections Dr. Bob.
The local schoolyard gang is gambling on the winner and you could really use
that extra cash. Luckily, you are able to hack into the mainframe of the school
and get a copy of the virtual machine that is used by
Dr. Bob to store the results. The desired information is in the
file /home/bob/flag.txt, easy as that.

dr_bob_e22538fa166acecc68fa17ac148dcbe2.tar.gz
mega.nz mirror
```

Download dr_bob_e22538fa166acecc68fa17ac148dcbe2.tar.gz and unzip and it was a VirtualBox image.

The only funny is, there is a snapshot. Boot up with the snapshot, usual Linux login.

Hackers to do list,

```
i. Reboot
ii. Grub
iii. Look for recovery, do a rw with init=/bin/bash
iv. Reboot
v. Login with root
```

We got root. Next thing is, cat /home/bob/flag.txt. Ok, expected nothing there.

Quick check on fstab, this is what we can see.

```
Partition 0:  / = no encryption
Partition 1: /home = crypto_LUKS
```

Additional Information: Running on ext4 and LLVM. Looks like we need decrypt crypto_LUKS.

Google says, VirtulBox RAMDUMP works this way

> $ VBoxManage debugvm SafeClone dumpvmcore --filename=getthekey

Usal trick getting key from RAMDUMP

```
$ aeskeyfind -v getthekey
FOUND POSSIBLE 128-BIT KEY AT BYTE 1c5f9148

KEY: 1fab015c1e3df9eac8728f65d3d16646

EXTENDED KEY:
1fab015c1e3df9eac8728f65d3d16646
20985b3a3ea5a2d0f6d72db525064bf3
4d2b5605738ef4d58559d960a05f9293
86648ae5f5ea7e3070b3a750d0ec35c3
40f2a495b518daa5c5ab7df515474836
f0a0a1cc45b87b698013069c95544eaa
f08f0de6b537768f35247013a0703eb9
e13d5b06540a2d89612e5d9ac15e6323
39c67d7e6dcc50f70ce20d6dcdbc6e4e
475952c32a95023426770f59ebcb6117
6eb6a22a4423a01e6254af47899fce50

CONSTRAINTS ON ROWS:
00000000000000000000000000000000
00000000000000000000000000000000
00000000000000000000000000000000
00000000000000000000000000000000
00000000000000000000000000000000
00000000000000000000000000000000
00000000000000000000000000000000
00000000000000000000000000000000
00000000000000000000000000000000
00000000000000000000000000000000

Keyfind progress: 100%
```

Login to to the VM using root, change IP. Enable openssh

Next, ssh into root, run this

```
root@bobby:~# echo "1fab015c1e3df9eac8728f65d3d16646" | xxd -r -p > mkf.key
root@bobby:~# cryptsetup luksAddKey --master-key-file mkf.key /dev/vg/home
```

After enter your passphrase, issue a reboot.
During boot up, it will ask for passphrase, enter you passphrase.

Login and we got the /home folder. Now, "cd /home" and the flag will be there.

```
root@bobby:~# cat /home/bob/flag.txt
You are very close :)
```

The only possibality is original flag is being deleted.

> root@bobby:~# dd if=/dev/mapper/vg-home_crypt of=paritiondump

We should able to see something, according to hack.lu ctf's flag format flag{theflag}

> root@bobby:~# strings paritiondump | grep flag\\{

The output is the flag !
> flag{v0t3_f0r_p3dr0}
