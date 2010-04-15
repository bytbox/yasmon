docs: yasmon.1 yasmond.1

yasmon.1: yasmon
	help2man -N ./yasmon > yasmon.1

yasmond.1: yasmond
	help2man -N ./yasmond > yasmond.1
