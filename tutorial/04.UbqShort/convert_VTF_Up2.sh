#!/bin/bash
mkdir allVTFs
mkdir OutputFiles
mv up_output/*output OutputFiles
cd up_output/
TOTAL=$(ls -l | grep -v ^d | wc -l)
i=1
for entry in $( ls ); do
	/beagle3/trsosnic/upside2-md/py/extract_vtf.py $entry $entry.vtf
	echo "$entry"
	echo "$i of $TOTAL"
	i=$((i+1))
done
mv *vtf ../allVTFs
cd ../

