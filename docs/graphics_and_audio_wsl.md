# Enabling Graphics

Heavily borrowed from [Mianzhi Wang](https://research.wmz.ninja/articles/2017/11/setting-up-wsl-with-graphics-and-audio.html)

WSL cannot display graphics on its own. The Linux subsytem needs a way of communicating with Windows. For this you need to install an X server on Windows. I use [Xming](https://sourceforge.net/projects/xming/). Once this is installed we need to tell Linux to connect to this display. The easiest way is to add the following command to the end of your `~/.bashrc` file which is executed each time a shell starts up.

```export DISPLAY=:0.0```

If all has worked, start the X server inside windows and then launch whichever graphic application you wanted from inside WSL (after reloading the shell). Try `gitk --all &` to view your git repo using a lightweight GUI.

# Enabling Audio

This project relies on audio, so we need to be able to access audio I/O from within WSL. This is actually quite tricky.