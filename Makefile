docs: yasmon.1 yasmond.1

yasmon.1: yasmon
	help2man -n "Yet another system monitor" -s 1 -N ./yasmon > yasmon.1

yasmond.1: yasmond
	help2man -n "Yet another system monitor - server" -s 1 -N ./yasmond > yasmond.1
