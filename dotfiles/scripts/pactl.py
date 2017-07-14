#!/usr/bin/env python3
# Copyright 2013 Canonical Ltd.
# Written by:
#   Zygmunt Krynicki <zygmunt.krynicki@canonical.com>

"""
Parser for `pactl list` output
"""

from argparse import ArgumentParser
from math import log10, floor, ceil
from pprint import pprint
from subprocess import check_output
import json
import os
import sys

import pyparsing as p


class Record:

    def __init__(self, header, entries):
        self.header = header
        self.entries = entries

    def __repr__(self):
        return "Record({!r}, {!r})".format(self.header, self.entries)

    @classmethod
    def from_tokens(cls, tokens):
        return cls(
            tokens['HEADER'],
            [token['entry'] for token in tokens['entry-list']])


class Entry:

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return "Entry({!r}, {!r})".format(self.name, self.value)

    @classmethod
    def from_tokens(cls, tokens):
        return cls(tokens['NAME'], tokens['value'])


def get_syntax():
    """
    Get the syntax suitable for parsing `pactl list` output

    The syntax parses valid text and produces a list of :class:`Record` objects
    """
    # The syntax uses indenting so a shared indent stack is required to parse
    # output properly. See indentedBlock() documentation for details
    indent_stack = [1]
    # VALUE
    # VALUE = p.Regex(".+").setResultsName("VALUE")
    property_value = (
        p.indentedBlock(
            p.Word(p.alphanums + ".").setResultsName("PROP_NAME")
            + p.Suppress('=')
            + p.QuotedString('"').setResultsName("PROP_VALUE"),
            indent_stack
        ).setResultsName("prop-value")
    )
    simple_value = p.ungroup(
        p.Combine(
            p.Regex(r".*")
            + p.Optional(
                p.indentedBlock(p.Regex(".+"), indent_stack)
            ),
            joinString='\n',
            adjacent=False
        )
    ).setResultsName("simple-value")
    value = p.Or(
        [property_value, simple_value]
    ).setResultsName("value")
    # NAME
    NAME = p.Regex("[^:]+").setResultsName("NAME")
    # entry: NAME ':' [VALUE] [indented<VALUE>]
    entry = (
        NAME + p.Suppress(":") + value
    ).setResultsName(
        "entry"
    ).setParseAction(
        Entry.from_tokens
    )
    # HEADER
    HEADER = p.restOfLine.setResultsName("HEADER")
    # record: HEADER '\n' indented<entry>
    record = (
        HEADER
        + p.Suppress(p.lineEnd)
        + p.indentedBlock(entry, indent_stack).setResultsName("entry-list")
    ).setResultsName(
        "record"
    ).setParseAction(
        Record.from_tokens
    )
    # record_list: record+
    record_list = p.OneOrMore(
        record
    ).setResultsName(
        "record-list"
    )
    syntax = record_list
    syntax.enablePackrat()
    return syntax


def show_text(text, hl_line=None, hl_col=None, context=None):
    """
    Show a body of text, with line and column markers.

    If both hl_line and hl_col are provided,
    they will be used to highlight the particular spot in the text.
    """
    lines = text.splitlines(True)
    if hl_line is not None and hl_col is not None and context is not None:
        window = slice(
            max(0, hl_line - context),
            min(hl_line + context, len(lines)))
    else:
        window = slice(0, len(lines))
    lines = lines[window]
    num_lines = len(lines)
    num_cols = max(len(line) for line in lines)
    col_lines_needed = floor(log10(num_cols))
    line_cols_needed = ceil(log10(window.start + num_lines))

    def print_col_ruler():
        for ndigit in range(col_lines_needed, -1, -1):
            print("      ", end='')
            print_it = False
            for colno in range(1, num_cols + 1):
                digit = (colno // 10 ** ndigit) % 10
                if digit > 0:
                    print_it = True
                print(digit if print_it else ' ', end='')
            print("")
        print("    +-" + "-" * num_cols)

    print_col_ruler()

    for lineno, line in enumerate(lines, window.start + 1):
        print(("{:" + str(line_cols_needed) + "d} |").format(lineno), end='')
        for c in line:
            if c.isprintable():
                print(c, end='')
            elif c == '\t':
                print('\x1B[30m\\t..\x1B[0m', end='')
            elif c == '\n':
                print('\x1B[36;1m\\n\x1B[0m', end='')
            else:
                print('\x1B[33m%r\x1B[0m' % c, end='')
        print()
        if lineno == hl_line:
            print('\x1B[37;1m_____' + hl_col * '_' + '^\x1B[0m')


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "--real-data", action='store_true', default=False,
        help="get real data from `pactl list`")
    parser.add_argument(
        "--dump", action='store_true', default=False,
        help="dump raw data after parsing`")
    parser.add_argument(
        "-c", "--context", default=3, type=int,
        help="show that many context lines when parse error is found")
    ns = parser.parse_args()
    if ns.real_data:
        env = os.environ.copy()
        env['LANG'] = 'C'
        pactl_text = check_output(
            ['pactl', 'list'], universal_newlines=True, env=env)
    else:
        pactl_text = """\
Sink #2
    State: SUSPENDED
    Name: alsa_output.pci-0000_01_00.1.hdmi-stereo-extra1
    Description: HDA NVidia Digital Stereo (HDMI)
    Driver: module-alsa-card.c
    Sample Specification: s16le 2ch 44100Hz
    Channel Map: front-left,front-right
    Owner Module: 4
    Mute: no
    Volume: 0: 100% 1: 100%
            0: 0.00 dB 1: 0.00 dB
            balance 0.00
    Base Volume: 100%
                 0.00 dB
    Monitor Source: alsa_output.pci-0000_01_00.1.hdmi-stereo-extra1.monitor
    Latency: 0 usec, configured 0 usec
    Flags: HARDWARE DECIBEL_VOLUME LATENCY SET_FORMATS 
    Properties:
        alsa.resolution_bits = "16"
        device.api = "alsa"
        device.class = "sound"
        alsa.class = "generic"
        alsa.subclass = "generic-mix"
        alsa.name = "HDMI 1"
        alsa.id = "HDMI 1"
        alsa.subdevice = "0"
        alsa.subdevice_name = "subdevice #0"
        alsa.device = "7"
        alsa.card = "1"
        alsa.card_name = "HDA NVidia"
        alsa.long_card_name = "HDA NVidia at 0xf6080000 irq 17"
        alsa.driver_name = "snd_hda_intel"
        device.bus_path = "pci-0000:01:00.1"
        sysfs.path = "/devices/pci0000:00/0000:00:01.0/0000:01:00.1/sound/card1"
        device.bus = "pci"
        device.vendor.id = "10de"
        device.vendor.name = "NVIDIA Corporation"
        device.string = "hdmi:1,1"
        device.buffering.buffer_size = "65536"
        device.buffering.fragment_size = "32768"
        device.access_mode = "mmap+timer"
        device.profile.name = "hdmi-stereo-extra1"
        device.profile.description = "Digital Stereo (HDMI)"
        device.description = "HDA NVidia Digital Stereo (HDMI)"
        alsa.mixer_name = "Nvidia GPU 40 HDMI/DP"
        alsa.components = "HDA:10de0040,1028053f,00100100"
        module-udev-detect.discovered = "1"
        device.icon_name = "audio-card-pci"
    Ports:
        hdmi-output-1: HDMI / DisplayPort 2 (priority: 5800, available)
    Active Port: hdmi-output-1
    Formats:
        pcm

Card #0
    Name: alsa_card.pci-0000_01_00.1
    Driver: module-alsa-card.c
    Owner Module: 4
    Properties:
        alsa.card = "1"
        alsa.card_name = "HDA NVidia"
        alsa.long_card_name = "HDA NVidia at 0xf6080000 irq 17"
        alsa.driver_name = "snd_hda_intel"
        device.bus_path = "pci-0000:01:00.1"
        sysfs.path = "/devices/pci0000:00/0000:00:01.0/0000:01:00.1/sound/card1"
        device.bus = "pci"
        device.vendor.id = "10de"
        device.vendor.name = "NVIDIA Corporation"
        device.string = "1"
        device.description = "HDA NVidia"
        module-udev-detect.discovered = "1"
        device.icon_name = "audio-card-pci"
    Profiles:
        output:hdmi-stereo: Digital Stereo (HDMI) Output (sinks: 1, sources: 0, priority. 5400)
        output:hdmi-surround: Digital Surround 5.1 (HDMI) Output (sinks: 1, sources: 0, priority. 300)
        output:hdmi-stereo-extra1: Digital Stereo (HDMI) Output (sinks: 1, sources: 0, priority. 5200)
        output:hdmi-surround-extra1: Digital Surround 5.1 (HDMI) Output (sinks: 1, sources: 0, priority. 100)
        off: Off (sinks: 0, sources: 0, priority. 0)
    Active Profile: output:hdmi-stereo-extra1
    Ports:
        hdmi-output-0: HDMI / DisplayPort (priority 5900)
            Part of profile(s): output:hdmi-stereo, output:hdmi-surround
        hdmi-output-1: HDMI / DisplayPort 2 (priority 5800)
            Part of profile(s): output:hdmi-stereo-extra1, output:hdmi-surround-extra1

Card #1
    Name: alsa_card.pci-0000_00_1b.0
    Driver: module-alsa-card.c
    Owner Module: 5
    Properties:
        alsa.card = "0"
        alsa.card_name = "HDA Intel PCH"
        alsa.long_card_name = "HDA Intel PCH at 0xf7730000 irq 46"
        alsa.driver_name = "snd_hda_intel"
        device.bus_path = "pci-0000:00:1b.0"
        sysfs.path = "/devices/pci0000:00/0000:00:1b.0/sound/card0"
        device.bus = "pci"
        device.vendor.id = "8086"
        device.vendor.name = "Intel Corporation"
        device.product.name = "Panther Point High Definition Audio Controller"
        device.form_factor = "internal"
        device.string = "0"
        device.description = "Built-in Audio"
        module-udev-detect.discovered = "1"
        device.icon_name = "audio-card-pci"
    Profiles:
        output:analog-stereo: Analog Stereo Output (sinks: 1, sources: 0, priority. 6000)
        output:analog-stereo+input:analog-stereo: Analog Stereo Duplex (sinks: 1, sources: 1, priority. 6060)
        input:analog-stereo: Analog Stereo Input (sinks: 0, sources: 1, priority. 60)
        off: Off (sinks: 0, sources: 0, priority. 0)
    Active Profile: output:analog-stereo+input:analog-stereo
    Ports:
        analog-output-speaker: Speakers (priority 10000)
            Part of profile(s): output:analog-stereo, output:analog-stereo+input:analog-stereo
        analog-output-headphones: Headphones (priority 9000)
            Part of profile(s): output:analog-stereo, output:analog-stereo+input:analog-stereo
        analog-input-microphone-internal: Internal Microphone (priority 8900)
            Part of profile(s): output:analog-stereo+input:analog-stereo, input:analog-stereo
        analog-input-microphone-dock: Dock Microphone (priority 7800)
            Part of profile(s): output:analog-stereo+input:analog-stereo, input:analog-stereo
        analog-input-microphone: Microphone (priority 8700)
            Part of profile(s): output:analog-stereo+input:analog-stereo, input:analog-stereo
        analog-input-linein: Line In (priority 8100)
            Part of profile(s): output:analog-stereo+input:analog-stereo, input:analog-stereo"""
    try:
        pactl_syntax = get_syntax()
    except Exception as exc:
        raise SystemExit(exc)
    try:
        tokens = pactl_syntax.parseString(pactl_text, True)
    except p.ParseBaseException as exc:
        if hasattr(exc, 'col') and hasattr(exc, 'lineno'):
            lineno = exc.lineno
            col = exc.col
        else:
            lineno = p.lineno(exc.loc, pactl_text)
            col = p.col(exc.loc, pactl_text)
        show_text(pactl_text, lineno, col, ns.context)
        raise SystemExit(exc)
    else:
        if ns.dump:
            # XXX: this is a bit insane but allows us to get
            # a dumb json structure out of what we parsed.
            pprint(
                json.loads(
                    json.dumps(
                        tokens.asList(),
                        default=lambda obj: obj.__dict__)))


if __name__ == "__main__":
    main()
