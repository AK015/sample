#!/bin/sh
filename=`echo $0 | sed -e "s/\.\///g" -e "s/\.sh//g" `
python ${filename}.py --cond ./json/${filename}.json