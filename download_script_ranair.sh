#!/bin/bash

getFilename="$PWD/captcha_file"
wget "https://cs7ns1.scss.tcd.ie/index.php?download=noresume_speed&shortname=ranair" -O $getFilename -q --show-progress
dir='images'

[[ ! -d $dir ]] && mkdir $dir;
for file in `awk -F',' '{print $1}' ${getFilename}`; do
	wget "https://cs7ns1.scss.tcd.ie/index.php?download=noresume_speed&shortname=ranair&myfilename=${file}" -P ${dir}/ -O "${dir}/$file" -q --show-progress
done
