#!/bin/sh
zip -X $(date "+%Y%m%d%H%M%S")-gerber.zip *.gbr *.drl
