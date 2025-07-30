import argparse
import json
from dataclasses import dataclass
from pathlib import Path

# See: https://github.com/mirror/ncurses/blob/87c2c84cbd2332d6d94b12a1dcaf12ad1a51a938/include/Caps
# for order of boolean capabilities

BOOL_CAPS = [
    'bw',
    'am',
    'xsb',
    'xhp',
    'xenl',
    'eo',
    'gn',
    'hc',
    'km',
    'hs',
    'in',
    'da',
    'db',
    'mir',
    'msgr',
    'os',
    'eslok',
    'xt',
    'hz',
    'ul',
    'xon',
    'nxon',
    'mc5i',
    'chts',
    'nrrmc',
    'npc',
    'ndscr',
    'ccc',
    'bce',
    'hls',
    'xhpa',
    'crxm',
    'daisy',
    'xvpa',
    'sam',
    'cpix',
    'lpix',
]

NUM_CAPS = [
    'cols',
    'it',
    'lines',
    'lm',
    'xmc',
    'pb',
    'vt',
    'wsl',
    'nlab',
    'lh',
    'lw',
    'ma',
    'wnum',
    'colors',
    'pairs',
    'ncv',
    'bufsz',
    'spinv',
    'spinh',
    'maddr',
    'mjump',
    'mcs',
    'mls',
    'npins',
    'orc',
    'orl',
    'orhi',
    'orvi',
    'cps',
    'widcs',
    'btns',
    'bitwin',
    'bitype'
]


@dataclass
class Header:
    magic_number: str
    names_nb: int
    boolean_nb: int
    numbers_nsi: int
    strings_nsi: int
    string_table_nb: int

def load_caps() -> dict[str, list[str]]:
    with open('caps.json', 'r') as f:
        caps = json.load(f)
    return caps

def load_terminfo_raw()->bytes:
    path = Path("/Applications/Ghostty.app/Contents/Resources/terminfo/78/xterm-ghostty")
    with open(path, 'rb') as f:
        tinf = f.read()
    return tinf

def get_header(tinf: bytes)->Header:
    header_vals = []
    for i in range(6):
        if i == 0:
            header_vals.append(oct(tinf[2*i] + tinf[2*i+1] * 256))
        else:
            header_vals.append(tinf[2*i] + tinf[2*i+1] * 256)
    return Header(*header_vals)

def section_names(tinf: bytes, header: Header)->list[str]:
    # the -1 is used to remove the ASCII NUL (\x00) that terminates
    # the section.
    names = tinf[12:12+header.names_nb-1].decode('ascii')
    return names.split('|')

def section_bool(tinf: bytes, header: Header, bool_caps:list[str])->list[str]:
    start = 12+header.names_nb
    return sorted(
        [
            cap for flag, cap in zip(tinf[start:start+header.boolean_nb+1], bool_caps)
            if flag == 1
        ]
    )

def section_numbers(tinf: bytes, header: Header, num_caps:list[str]):
    # possibly skips a byte so that number section starts on even byte
    start = 12 + header.names_nb + header.boolean_nb
    if start % 2 == 1:
        assert tinf[start] == 0, "Expected null byte as offset"
        start += 1

    nums = []
    for i in range(header.numbers_nsi):
        blo, bhi = tinf[start+2*i], tinf[start+2*i+1]
        if oct(blo) == '0o377' and oct(bhi) == '0o377':
            # capabilities is missing
            continue
        nums.append((num_caps[i], blo + 256*bhi))

    return sorted(nums, key=lambda x: x[0])
    
def section_strings(tinf: bytes, header: Header, strings_cap: list[str], raw: bool=False):
    start = (
        12 +
        header.names_nb +
        header.boolean_nb +
        2 * header.numbers_nsi
    )

    if start % 2 == 1:
        start += 1

    # first, load the strings table
    start_alt = start + 2 * header.strings_nsi
    strings_table = tinf[start_alt:]
    #breakpoint()

    # index into the string table
    res = []
    for i in range(header.strings_nsi):
        blo, bhi = tinf[start+2*i], tinf[start+2*i+1]
        if oct(blo) == '0o377' and oct(bhi) == '0o377':
            # capabilities is missing
            continue
        offset = blo + 256*bhi
        ii = 0
        try:
            while strings_table[offset+ii] != 0:
                ii += 1
        except:
            breakpoint()
        
        val = strings_table[offset:offset+ii]

        if not raw:
            if len(val) == 1 and ord(val) <= 31:
                # this is an escape sequence, convert to printable representation
                val = '^{val}'.format(val=chr(ord(val)+0x40))
            else:
                # if any element of the list of codepoints is '\x1b',
                # convert to the \E representation
                def _render_non_printable(c):
                    # if printable: just render the regular ascii representation
                    # else: prints the octal preceded by '\'. e.g. 0o177 -> \177
                    if c <= 31 or c >= 127:
                        oct_repr = oct(c).replace('0o','').zfill(3)
                        return f'\\{oct_repr}'
                    else:
                        return chr(c)
                val = ''.join(
                    [r'\E' if val_i == 27 else _render_non_printable(val_i) for val_i in val]
                )
        res.append((strings_cap[i], val))
    return sorted(res, key=lambda x: x[0])

def format_entry(names, bools, nums, strs, line_length=70):
    lines = []
    lines.append('|'.join(names))
    lines.append(','.join(bools))
    lines.append(','.join(['#'.join([a, str(b)]) for a,b in nums]))

    line = ''
    for cap, val in strs:
        if line == '':
            line += f'{cap}={val},'
        else:
            proto_line = line + f' {cap}={val},'
            if len(proto_line) <= line_length:
                line = proto_line
            else:
                lines.append(line)
                line = f'{cap}={val},'

    lines.append(line)
    return lines

def main():
    tinf = load_terminfo_raw()
    header = get_header(tinf) # reads first 12 bytes (0-11)

    caps = load_caps()
    names = section_names(tinf, header)
    bools = section_bool(tinf, header, caps['bool'])
    nums = section_numbers(tinf, header, caps['num'])
    strs = section_strings(tinf, header, caps['string'])

    r = format_entry(names, bools, nums, strs, line_length=58)

    print('\n\t'.join(r))
    
if __name__ == '__main__':
    main()


