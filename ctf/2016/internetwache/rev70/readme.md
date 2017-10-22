Description:

> My friend sent me this file. He told that if I manage to reverse it, I'll have access to all his devices. My misfortune that I don't know anything about reversing :/

Did not do so much with RE. F5 ftw.

```
int __fastcall handle_task(int result, char *a2)
{
  signed int v2; // ST0C_4@5
  char *s; // [sp+0h] [bp-1Ch]@1
  int v4; // [sp+4h] [bp-18h]@1
  size_t i; // [sp+8h] [bp-14h]@2
  unsigned int v6; // [sp+Ch] [bp-10h]@1

  v4 = result;
  s = a2;
  v6 = 0;
  switch ( result )
  {
    case 0:
      for ( i = 0; strlen(s) > i; ++i )
        v6 += (unsigned __int8)s[i];
      v2 = v6 / strlen(s);
      printf("%s", "Here's your 1. block:");
      if ( v2 <= 35 )
      {
        printf("%s", "IW{");
        putchar(83);
        result = printf("%c%c\n", 46, 69);
      }
      else
      {
        result = puts("I{WAQ3");
      }
      break;
    case 1:
      printf("%s", "Here's your 2. block:");
      if ( (unsigned __int8)*s % (signed int)(unsigned __int8)s[1] == 65 )
      {
        printf("%s", ".R.");
        putchar(86);
        result = printf("%c%c\n", 46, 69);
      }
      else
      {
        result = puts("WI{QA3");
      }
      break;
    case 2:
      printf("%s", "Here's your 3. block:");
      if ( !strcmp(s, "1337") )
        result = puts(".R>=F:");
      else
        result = printf("%c%s%c\n", 46, "Q.D.Q", 33, s, v4);
      break;
    case 3:
      if ( *a2 )
        result = printf("%c%s%c\n", 65, ":R:M", 125, a2, result);
      break;
    default:
      return result;
  }
  return result;
}

```
C with style

```
#include <stdio.h>

int result;

int main()
{

        printf("%s", "IW{");
        putchar(83);
        printf("%c%c\n", 46, 69);

        printf("%s", ".R.");
        putchar(86);
        printf("%c%c\n", 46, 69);

        puts(".R>=F:");

	      putchar(65);
	      printf("%s",":R:M");
        putchar(125);

}

```

After compile and run it.

```
xwings@ubuntu:~/rev70/task$ ./test
IW{S.E
.R.V.E
.R>=F:
A:R:M}
```

We got the flag.

> IW{S.E.R.V.E.R>=F:A:R:M}
