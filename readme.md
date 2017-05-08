# simple-ss-manager-manager
Simple wrapper for ss-manager; auto reload configure; a tiny handmake managing shell.
Targeting for auto startup ss-manager as well as reloading all configurations in `~/.shadowsocks`, and remove the need of `nc` with `-Uu` support.

1. Place the `mync.py` file anywhere you like
2. Change the path of `mync.py` in `ss-manager.service`
3. Copy `ss-manager.service` to `/usr/lib/systemd/system`
4. Don't forget to run `systemctl enable`!
5. Enjoy!

