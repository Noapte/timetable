#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
from main import app

parser = argparse.ArgumentParser()
parser.add_argument('--debug', action='store_true')


if __name__ == '__main__':
    args = parser.parse_args()
    app.run(debug=args.debug)
