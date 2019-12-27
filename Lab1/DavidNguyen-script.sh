#!/bin/sh

for item in *
do 
	
		exec < $item

		count=0
	    temp=0
		while read line
			do 
				count=`expr $count + 1`
				temp=`expr $count % 2`
				if [ $temp -eq 0 ] 
					then 
							echo $item: $line
					fi 
	done	

done


