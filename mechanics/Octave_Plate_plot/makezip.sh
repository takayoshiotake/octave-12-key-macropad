#!/bin/sh
zip -X $(date "+%Y%m%d%H%M%S")-plate-gerber.zip *.gbr *.drl
