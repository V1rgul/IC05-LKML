#!/bin/bash
DIR=$(dirname "$(readlink -f "$0")")
TODATE="$DIR/js/toDate.js"

function tocsv {
	echo "$(realpath $1)"
	EXECJS="$3"
	#echo "exec:$EXECJS"

	# convert html table to csv, remove 'Re: ' from mails
	cat "$1" | grep -i -e '</\?TABLE\|</\?TD\|</\?TR\|</\?TH' | sed 's/^[\ \t]*//gI' | tr -d '\n' | sed 's/<\/TR[^>]*>/\n/gI'  | sed 's/<\/\?\(TABLE\|TR\)[^>]*>//gI' | sed "s/'//g" | sed "s/,//g" | sed 's/^<T[DH][^>]*>\|<\/\?T[DH][^>]*>$//gI' | sed 's/<\/T[DH][^>]*><T[DH][^>]*>/'"','"'/gI' | sed 's/<[^>]*>//g' | sed "s/^/'/g" | sed "s/$/'/g" | grep "^' '\|^'\[New\]'" | sed 's/"//g' | sed 's/Re: //g' | "$EXECJS" "$1" >> $2

	#echo "DIR:$DIR" 
	#"$DIR/toDate.js" "$2.temp" "$2"
	#cat "$2.temp" >> "$2"
}

function all_tocsv {
	# convert all html files to csv
	echo > "$2.temp"
	export -f tocsv
	find "$1" -type f -exec 'bash' '-c' 'tocsv "{}" '"$2.temp"' '"$TODATE" ';'

	# filter csv so all rows have 3 col
	awk -F "','" 'NF == 4 { print $0 }' "$2.temp" > "$2"
	rm -f "$2.temp"
}

function togephicsv {
	# convert so gephi can open it properly
	cp "$1" "$2"
	sed -i "s/','/\t/g" "$2"
	sed -i "s/^'//g" "$2"
	sed -i "s/'$//g" "$2"
	mv "$2" "$2.temp"
	echo -e "New\tSubject\tAuthor" > "$2"
	cat "$2.temp" >> "$2"
	rm -f "$2.temp"
}

all_tocsv "$1" "$2"
