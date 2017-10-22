Description:

> My friend sent me this file. He told that if I manage to reverse it, I'll have access to all his devices. My misfortune that I don't know anything about reversing :/

Did not do so much with RE. F5 ftw.

```
__int64 __fastcall sub_40079C(int a1, int *a2)
{
  int v2; // ecx@1
  __int64 result; // rax@1
  int v4; // [sp+10h] [bp-40h]@1
  int v5; // [sp+14h] [bp-3Ch]@1
  int v6; // [sp+18h] [bp-38h]@1
  int v7; // [sp+1Ch] [bp-34h]@1
  int v8; // [sp+20h] [bp-30h]@1
  int v9; // [sp+24h] [bp-2Ch]@1
  int v10; // [sp+28h] [bp-28h]@1
  int v11; // [sp+2Ch] [bp-24h]@1
  int v12; // [sp+30h] [bp-20h]@1
  int v13; // [sp+34h] [bp-1Ch]@1
  int v14; // [sp+38h] [bp-18h]@1
  int v15; // [sp+3Ch] [bp-14h]@1
  int v16; // [sp+40h] [bp-10h]@1
  int v17; // [sp+44h] [bp-Ch]@1
  int v18; // [sp+48h] [bp-8h]@1

  v4 = 4846;
  v5 = 4832;
  v6 = 4796;
  v7 = 4849;
  v8 = 4846;
  v9 = 4843;
  v10 = 4850;
  v11 = 4824;
  v12 = 4852;
  v13 = 4847;
  v14 = 4818;
  v15 = 4852;
  v16 = 4844;
  v17 = 4822;
  v18 = 4794;
  v2 = (*(&v4 + a1) + *a2) % 4919;
  result = (unsigned int)v2;
  *a2 = v2;
  return result;
}
```
Wrote a quick ruby script to brute force the flag.

```
#!/usr/bin/ruby

# ruby -e 'print ((4832 + 87) % 4919)' ; should be zero

encstrs = Array[4846,4832,4796,4849,4846,4843,4850,4824,4852,4847,4818,4852,4844,4822,4794]


encstrs.each do |encstr|
	i = 0
	num = 255
	while i < num  do
		ifzero = (((encstr + i) % 4919))
		if ifzero == 0
			puts(i.chr)
		end
		i +=1
	end
end
```

We got the flag.

> IW{FILE_CHeCKa}
