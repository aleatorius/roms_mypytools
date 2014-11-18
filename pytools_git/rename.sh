#!/bin/bash 
pathout=/global/work/mitya/run/Arctic-20km/archive_2005_rename/
pathin=/global/work/mitya/run/Arctic-20km/archive_2005
set -x
for file in "$@"
do
    echo $file
  
    if [ -f $file ]; then
        echo "file exists"
        echo $file
        if foo="$(ncdate_re.py $file)"; then
            echo "python works", $foo
            read -a array <<< $foo
            echo ${array[0]}, ${array[1]}, ${array[2]}
            fileout=${pathout}${file%.*}_${array[2]}.${file#*.}
	    echo $fileout
            if [ -f $fileout ]; then
		echo 'A remote file already exists, do nothing'
            else
                echo "Proceed with  cp-copying of this file"
		if mv $file $fileout; then
		    echo "success"
		else
                    echo "cp doesn't work!"
                    exit 1
		fi
            fi
        else
            echo "Cannot execute python! Aborting." 1>&2
            exit 1
        fi
    else
        echo "A local file does not exist"
    fi
done


set +x

exit