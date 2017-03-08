#!/usr/bin/python
import sys
import re


class OptionParse(object):
    def __init__(self, args=None):
        self.__table = None
        self.args = None
        self.argc = 0
        self.params = None
        self.short = []
        self.long = []

        self.reset(args)

    def reset(self, args=None):
        self.__table = None
        self.args = args if args and len(args) > 0 else sys.argv

        self.argc = len(self.args)
        self.params = self.args[2:] if self.argc > 2 else []

        pattern = self.args[1] if self.argc >= 2 else ''
        pattern = pattern.strip('"').strip("'")

        short_line = re.sub(r'(\[[^\[\]]+\])', '', pattern)
        long_line = re.findall(r'(\[[^\[\]]+\])', pattern)

        self.short = [x.strip() for x in short_line]
        for x in long_line:
            cmd = x.strip('[').strip(']')
            self.long.append(cmd)

    def parse2str(self):

        if isinstance(self.__table, dict):
            table = self.__table
        else:
            table = self.parse2dict()

        cmdstr = ''
        if not isinstance(table, dict):
            return cmdstr

        for k, v in table.iteritems():
            if v:
                cmdstr += "%s:%s  " % (k, v)
            else:
                cmdstr += '%s  ' % (k)
        return cmdstr

    def parse2dict(self):
        if self.__table:
            return self.__table

        self.__table = {}

        slen = len(self.short)
        plen = len(self.params)

        if slen <= 0 or plen <= 0:
            return ''

        count = 0
        while count < plen:
            item = self.params[count].strip()

            if item.startswith('--'):

                for e in self.long:
                    lkey = ''
                    skey = ''
                    val = item[item.find('=') + 1:] if item.find('=') >= 0 else ''

                    lopt = item.strip('--')
                    lopt = lopt[0:lopt.find('=')] if lopt.find('=') >= 0 else lopt

                    si = e.find('#')
                    vi = e.find(':')

                    ne = e.strip(':')
                    if si >= 0:

                        a = ne[0:si].strip()
                        b = ne[si + 1:len(e)].strip()
                        if len(a) > len(b):
                            lkey, skey = (a, b)
                        else:
                            lkey, skey = (b, a)
                    else:
                        lkey = ne

                    if lopt == lkey:
                        if si > 0:
                            if skey and len(skey) > 0:
                                self.__table['-%s' % (skey)] = val
                            else:
                                pass
                        else:
                            self.__table['--%s' % (lkey)] = val
                    else:
                        pass

            elif item.startswith('-'):
                scount = 0

                while scount < slen:
                    sopt = self.short[scount]
                    nopt = self.short[scount + 1] if scount + 1 < slen else ''

                    key = item[1:2] if len(item) >= 2 else ''
                    val = ''

                    # if the option is exist, parse the key and value.
                    if key == sopt:
                        if nopt == ':':
                            if len(item) <= 2:
                                nparam = self.params[count + 1] if count + 1 < plen else ''
                                if not nparam.startswith('-'):
                                    val = nparam
                                    count += 1
                                else:
                                    val = ''
                            else:
                                val = item[2:]
                        else:
                            pass
                        self.__table['-%s' % key] = val
                    else:
                        pass
                    scount += 1
                    # end if about parsing key and value
            else:
                self.__table[item] = None
            count += 1

        return self.__table

    def get(self, key, default=''):
        table = self.__table
        if not key or not isinstance(table, dict):
            return default
        if table.has_key(key):
            return table[key]
        else:
            return default

    def exists(self, cmd):
        table = self.__table
        if isinstance(table, dict):
            return table.has_key(cmd)
        else:
            return False


if __name__ == '__main__':
    opts = OptionParse(sys.argv)
    print opts.parse2str()
