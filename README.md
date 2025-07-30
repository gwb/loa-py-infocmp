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


## Further notes

The `caps.py` in the repo is used to generate the `cap.json` file, a list of the capabilities, 
as listed in ncurses `caps` file. You don't need to run it. If you do want to run it, then you 
need to copy ncurses's [caps file](https://github.com/mirror/ncurses/blob/87c2c84cbd2332d6d94b12a1dcaf12ad1a51a938/include/Caps) into the directory and then

```
python3 caps.py
```


## Limitations

This is a very brittle implementation. It works for some terminfo files but not 
others. For instance, it works fine for ghostty's terminfo file and the `vt100` terminfo file 
(found `/usr/share/terminfo/76/vt100` on my mac), but not for the `iterm2` terminfo files. This 
might have to do with extended capabilities, etc..


