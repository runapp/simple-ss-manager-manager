# simple-ss-manager-manager
Simple wrapper for ss-manager; auto reload configure; a tiny handmake managing shell.

Targeting for auto startup ss-manager as well as reloading all configurations in `~/.shadowsocks`, and remove the need of `nc` with `-Uu` support.

### Usage

1. Place the `mync.py` file anywhere you like
2. `chmod +x mync.py`
3. Run `./mync.py install`
4. Don't forget to run `systemctl enable ss-manager`
5. Enjoy!

