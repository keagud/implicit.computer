+++
title="Lesser-Known Python Goodies"
date=2024-04-16
slug="python-goodies"
[taxonomies]
tags=["python", "programming", "100DaysToOffload"]
+++


Python is famously an easy language  to learn, but it's a hard language to *really* learn because there's so just much of it; Python's standard library has over *300* modules as of version 3.11! [^1] Knowing a programming language in depth includes knowing how to effectively wield its standard library to solve problems, but for Python that's a tough ask. 

In practice, you learn the subset of the standard library that's most useful in your day-to-day, and that's fine, but it also means there's potentially whole swaths of useful stuff you could be taking advantage of, but simply never encountered. So, here's my list of Python features you might not know about. Here are my selection criteria:

1. I've excluded things I've already seen a lot of coverage for, for example the very useful [`http.server`](https://docs.python.org/3/library/http.server.html)
2. These must be tools I've actually used to solve a real world problem. It's both very cool and not well known that Python has a full [turtle graphics library](https://docs.python.org/3/library/turtle.html), but I've never needed it in practice.



## Unicode Literals

First, a general trick rather than a module. You likely knew that Python's `str` type supports Unicode, and you maybe also knew that you can specify Unicode codepoints with the `\u` prefix:

```python
>"\u0D9E"
'ඞ'
```

But did you know [you can also include Unicode by name?](https://docs.python.org/3/howto/unicode.html#the-string-type)[^2]

```python
>"\N{MAN IN BUSINESS SUIT LEVITATING}"
'🕴️'
```

I haven't run into too many uses for this, but I *did* once need to include a [ñ](https://en.wikipedia.org/wiki/%C3%91) character in a string, and specifying it directly as `"\N{LATIN SMALL LETTER N WITH TILDE}"` rather than copy-pasting it made me feel very smug at least.

## Text Wrapping

Sure, you can write a text wrapping function in no time, it's not hard. And if you've done any amount of low-ish level text management (like for [curses](https://en.wikipedia.org/wiki/Curses_(programming_library))-style interfaces) you've probably gotten a lot of practice re-implementing text wrap. But now that you know about the [textwrap](https://docs.python.org/3/library/textwrap.html#module-textwrap) module, you're free to spend that time somewhere else. Go ahead, I release you. 


## IP Address Handling
Stop using strings for IP addresses! Stop it! We have the [ipaddress](https://docs.python.org/3/library/ipaddress.html#module-ipaddress) module for that! Don't make me come over there!

This is one of those things that I imagine most Python users will never need, but for automating network configuration stuff it's a godsend. 

```python
>>> from ipaddress import ip_address, IPv4Network
>>> ip = ip_address("192.168.0.1")
>>> ip.is_private # True
>>> ip.is_loopback # False


>>> network = IPv4Network("192.168.0.0/24")
>>> network.netmask # 255.255.255.0
>>> network.num_addressed # 256

>>> hosts = list(network.hosts())
>>> hosts[0] # IPv4Address('192.168.0.1')
>>> hosts[-1] # IPv4Address('192.168.0.254')
```

There's equivalent functionality for IPv6 as well, plus lots of other handy stuff - `IPv6Address` has a `sixtofour` property that can extract an IPv4 address from 6to4, for example.


## Web Browser Control

Finally, the [webbrowser](https://docs.python.org/3/library/webbrowser.html#module-webbrowser) module provides functions to open a url in the default web browser. That's it, really; it's not a proper browser automation toolkit like [Selenium](https://www.selenium.dev/), but often you don't need all that power anyway. If you think outside the box, even the most basic functions of a web browser can be tremendously useful.

Here's an anecdote to  illustrate the versatility of `webbrowser`: once upon a time I was asked to write a script to take user-provided data and do various CRUD shenanigans with it -  nothing too crazy, but there were some unique constraints. Namely, no external dependencies whatsoever[^3] while remaining approachable to non-technical users. My solution was to use `webbrowser.open` and `http.server` simultaneously to create the world's smallest technically-a-web-app that, to the user, just presented as a friendly webpage with a form.[^4] That's an extreme example, but my point is that a web browser can be a surprisingly versatile component of your scripting toolkit. 


---

[^1]: You can check this for any version after 3.10 with  `python3 -c 'import sys; print(len(sys.stdlib_module_names))'`. For 3.11.9 it prints 305.

[^2]: You can also include Unicode in identifier names, but emoji doesn't seem to work, at least not in CPython 😥

[^3]: Except `requests`, that is. This needed to be maximally portable with no setup, and the only guarantee for the runtime environment was that `requests` would be there, and that Some Kind Of Web Browser would be there. Everything else had to come from the standard library.

[^4]: Yes, I could have used tkinter to make a proper GUI, but this was a time-sensitive thing and I can hack together a basic webpage before I would have even finished skimming the tkinter docs.
