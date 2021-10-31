#!/bin/bash

wget -O png_filename.txt "https://cs7ns1.scss.tcd.ie/index.php?download=noresume_speed&shortname=mukhopat"

file='png_filenames.txt'

while read line
do
	prefix="wget -O "
	filename=$line
	URL=" https://cs7ns1.scss.tcd.ie/index.php?download=noresume_speed&shortname=mukhopat&myfilename="
	final_string=$prefix$filename$URL$filename
	`$final_string`
done < $file
