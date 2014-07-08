gvfs_automount.py
=========

Overview
--
 
Automatically mounts removable media (eg: CD-ROMS, USB-drives, etc.) upon
insertion/connection. Also generates a desktop notification when it mounts
something.


Usage
--

It's a good idea to pipe stdout to a file or to `/dev/null`, as Python tends to
freak out if stdout gets closed. From something like an .xsession file you'd
want to do something like:

    ~/bin/gvfs_automount.py >/dev/null &

If you use i3, like I do, you can add something like this to your `.i3/config`
instead:

    exec --no-startup-id ~/bin/gvfs_automount.py >/dev/null

(These both assume you've put the script in ~/bin -- adjust the path
accordingly.)


Why I Wrote This
--

I use the [i3 tiling window manager](http://i3wm.org/) on top of a Gnome
session.  My setup is a based on [this
one](http://blog.hugochinchilla.net/2013/03/using-gnome-3-with-i3-window-manager/),
but without a Gnome panel:

    # /usr/share/xsessions/gnome-i3.desktop
    [Desktop Entry]
    Name=GNOME with i3
    Comment=A GNOME fallback mode session using i3 as the window manager.
    Exec=gnome-session --session=i3
    TryExec=gnome-session
    Icon=
    Type=Application


    # /usr/share/gnome-session/sessions/i3.session
    [GNOME Session]
    Name=gnome-i3
    RequiredComponents=gnome-settings-daemon;i3;

When I upgraded my system from Ubuntu 13.10 to 14.04, auto-mounting
mysteriously stopped working. You can see the [Ask Ubuntu question I asked
about
this](http://askubuntu.com/questions/491416/how-to-get-gvfs-to-automount-removable-devices-when-not-using-unity-or-gnome-she)
for more details.

Since that question got no answers, I looked through [the source for
`gvfs-mount`](http://www.linuxfromscratch.org/blfs/view/svn/gnome/gvfs.html),
read [some Python GTK+ 3 documentation](
https://python-gtk-3-tutorial.readthedocs.org/en/latest/index.html), and wrote
this script.
