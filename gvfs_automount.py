#!/usr/bin/env python3
# coding=utf-8

"""
Auto-mounter for gvfs.

Automatically mounts removable media (eg: CD-ROMS, USB-drives, etc.) upon
insertion/connection.
"""

import argparse
import sys

from gi.repository import Gio
from gi.repository import GObject
from pprint import pprint

__author__  = 'Laurence Gonsalves <laurence@xenomachina.com>'

def dump_to_stdout(*args, **kwargs):
    pprint({"Args": args})
    pprint({"KWArgs": kwargs})

def print_volume_identifiers(volume):
    for identifier in volume.enumerate_identifiers():
        print("    %s: %r" % (identifier, volume.get_identifier(identifier)))

def on_volume_added(vm, volume, _):
    print("\nVOLUME ADDED")
    print_volume_identifiers(volume)
    should_automount = volume.should_automount()
    print("    should_automount: %s" % should_automount)
    if should_automount:
        mount_op = Gio.MountOperation()
        # TODO: g_signal_connect (op, "ask_password", G_CALLBACK (ask_password_cb), NULL);
        # TODO: connect to the "aborted" signal? Any others?
        volume.mount(0, mount_op, None, on_volume_mounted, mount_op)

def on_volume_mounted(volume, async_result, mount_op):
    if volume.mount_finish(async_result):
        print("MOUNTED VOLUME")
        print_volume_identifiers(volume)


class UserError(Exception):
    def __init__(self, message):
        self.message = message

def create_parser():
    description, epilog = __doc__.strip().split('\n', 1)
    parser = argparse.ArgumentParser(description=description, epilog=epilog,
            formatter_class=argparse.RawDescriptionHelpFormatter)
    return parser

def main(args):
    vm = Gio.VolumeMonitor.get()
    connections = []
    connections.append(vm.connect("volume-added", on_volume_added, None))
    GObject.MainLoop().run()

if __name__ == '__main__':
    error = None
    parser = create_parser()
    try:
        args = parser.parse_args()
        main(args)
    except FileExistsError as exc:
        error = '%s: %r' % (exc.strerror, exc.filename)
    except UserError as exc:
        error = exc.message

    if error is not None:
        print(('%s: error: %s' % (parser.prog, error)), file=sys.stderr)
        sys.exit(1)
