#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from zipfile import ZipFile
from io import TextIOWrapper
from datetime import datetime, timezone
from typing import Iterable

from pigra.parser import IgraParser
from pigra.utils import jsonfmt


def main():
    parser = IgraParser()
    jsonfmt("[")  # open json array
    for sounding in parser.parse():
        jsonfmt(sounding.to_json(), indentlvl=1)
    jsonfmt("]")  # close json array
    print(parser.stats, file=sys.stderr)


if __name__ == '__main__':
    main()
