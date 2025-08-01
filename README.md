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


The `caps` file has some instruction on when to stop parsing the file.. but I've found that 
if I indeed stop parsing there, then I would get results that differ from `infocmp`.. An 
example is with the `iterm2` terminfo file (located here on my system: `/Applications/iTerm.app/Contents/Resources/terminfo/78/xterm-256color`).


## Limitations

- This has not been thoroughly tested. I've spot checked the results for a few terminals,
  including ghostty and the results look reasonable. I have checked iterm2 and vt100 very 
  cursorily and it seems to be reasonable as well. 
  
- It would be helpful to right a script to compare the output of ncurses `infocmp` versus 
  my own implementation on the content of `/usr/share/terminfo/*`.


