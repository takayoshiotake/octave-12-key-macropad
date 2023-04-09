#!/bin/sh
zip -X $(date "+%Y%m%d%H%M%S")-gerber.zip \
  *.gb* *.gm1 *.gt* *.drl
