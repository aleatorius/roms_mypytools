#!/usr/bin/sh


source /etc/profile.d/modules.sh
module swap intelcomp/12.0.5.220 intelcomp/13.0.1
module load mpt/2.06 python/2.7.3 netcdf/4.3.0 


set -x
datstamp=`date +%Y_%m_%d_%H_%M`
pathout=/global/work/mitya/arctic20_test_jens/
pathin=${PWD#*}
echo $pathin
#WORK=/work/mitya
#homedir=/home/ntnu/mitya

#EXPECTED_ARGS=2
#E_BADARGS=65

#if [ $# -ne $EXPECTED_ARGS ]
#then
#  echo "Usage: `basename $0` {arg1 arg2}"
#  exit $E_BADARGS
#fi

#echo $1 $2  ' -> echo $1 $2'
#args=("$@")
#echo ${args[0]} ${args[1]} ' -> args=("$@"); echo ${args[0]} ${args[1]}'
#echo $@ ' -> echo $@'
#echo Number of arguments passed: $# ' -> echo Number of arguments passed: $#' 

#echo {$i..$j}

for file in "$@"
do
    echo $file
   # file=$l
    if [ -f $file ]; then
	echo "file exists"
	echo $file
	if foo="$(ncdate_re.py $file)"; then 
	    echo "python works", $foo
	    read -a array <<< $foo
	    echo ${array[0]}, ${array[1]}, ${array[2]} 
	    fileout=${pathout}${file%.*}_${array[2]}.${file#*.}
	    if ssh mitya@stallo.uit.no stat $fileout \> /dev/null 2\>\&1; then
		echo 'A remote file already exists, do nothing'
	    else
		echo "Proceed with  ssh-copying of this file"
		if scp $file mitya@stallo.uit.no:$fileout; then
		    rm $file
		else
		    echo "scp doesn't work!"
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
