# simple-ss-manager-manager
Simple wrapper for ss-manager; auto reload configure; a tiny handmake managing shell.

Targeting for auto startup ss-manager as well as reloading all configurations in `~/.shadowsocks`, and remove the need of `nc` with `-Uu` support.

### Deployment

1. Place the `mync.py` file anywhere you like
2. `chmod +x mync.py`
3. Run `./mync.py install`
4. Don't forget to run `systemctl enable ss-manager`
5. Enjoy!


### Managing

To manager `ss-server` slaves, just run `./mync.py`, and
 - Type `p` for ping
 - Type `a1abc` or `a 1 abc` to add a slave on port `baseport+1` with password `abc`
 - Type `r1` or `r 1` for deleting slave on port `baseport+1`
 - Spaces just don't matter, `a      10barfoo` also works
 - Check code for more details

Attention: Don't move `mync.py` after step 3. Or you may need to run `install` again.

