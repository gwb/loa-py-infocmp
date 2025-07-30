# Less of an Infocmp

This is a small python implementation of a very small subset of the unix `infocmp` utility 
(distributed as part of the ncurses library). I wrote it purely for educational purposes.

The `infocmp` utility parses the compiled terminfo file describing the capabilities of your 
terminal (emulator) and prints them to the screen. I was mostly interested in better understanding 
how the binary format was parsed, etc..

## Usage

```
python3 main.py
```

will check the TERMINFO environment variable and, if it exists, it will parse the terminfo 
file it finds there and print its content to the screen, in a format similar to `infocmp`.


```
python3 main.py --path /path/to/terminfo
```

allows to point to an explicit terminfo file to parse.


## Limitations

This is a very brittle implementation. It works for some terminfo files but not 
others. For instance, it works fine for ghostty's terminfo file and the `vt100` terminfo file 
(found `/usr/share/terminfo/76/vt100` on my mac), but not for the `iterm2` terminfo files. This 
might have to do with extended capabilities, etc..


