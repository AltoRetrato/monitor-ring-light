#!/usr/bin/python3
# -*- coding: utf-8 -*-
# By Ricardo Mendonça Ferreira - ric@mpcnet.com.br
#
# 2021.03.06  1st release.
# 2020.06.22  1st version.

import json
import errno


class Cfg(dict):

    def __init__(self, fn="config.json", log=None, default=None):
        self.fn  = fn
        self.log = log
        if default:
            # Oops! "TypeError" on MicroPython! :(
            # "Cause: Subclassing native classes is not fully supported in MicroPython."
            # http://docs.micropython.org/en/latest/genrst/builtin_types.html?highlight=subclassing#exception-init-method-does-not-exist
            self.update(default) 


    def load(self, fn=None, ignore_not_found=False):
        """ Load data from a JSON file, optionally logging any error found. """
        fn = fn or self.fn
        try:
            with open(fn) as fh:
                data = json.load(fh)
                self.clear()
                self.update(data)
        except Exception as e:
            if e.args[0] == errno.ENOENT:
                if ignore_not_found:
                    return True
                msg = "[Cfg.load] Could not open file [{}]: {}".format(fn, e)
            else: 
                msg = "[Cfg.load] Exception reading configuration from [{}]: {}".format(fn, e)
            if self.log:
                  self.log(msg)
            else: print(msg)
            return False
        return True


    def save(self, fn=None):
        """ Save data to a JSON file, optionally logging any error found. """
        fn = fn or self.fn
        try:
            with open(fn, "w") as fh:
                json.dump(self, fh)
        except Exception as e:
            msg = "[Cfg.save] Exception saving configuration file [{}]: {}".format(fn, e)
            if self.log:
                  self.log(msg)
            else: print(msg)
            return False
        return True


#if __name__ == "__main__":
#    cfg = Cfg()
#    cfg["key"] = "value"
#    cfg.save()
#    cfg2 = Cfg()
#    cfg2.load()
#    print(cfg2)
