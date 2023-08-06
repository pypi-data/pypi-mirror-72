#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys


def main():
    from ipcn.geo import query_ip_location

    for ip_arg in sys.argv[1:]:
        try:
            print("%s\t\t%s" % (ip_arg, query_ip_location(ip_arg)))
        except Exception as err:
            print("%s\t\tERROR:%s" % (ip_arg, err))
            pass


if __name__ == '__main__':
    main()
    pass
