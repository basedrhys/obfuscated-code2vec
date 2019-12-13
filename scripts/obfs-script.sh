#!/usr/bin/env bash
###########################################################
INPUT_DIR=java-large
OUTPUT_DIR=java-large-test
NUM_PARTITIONS=1
NUM_THREADS=13
ARGS="-Xmx13g"

###########################################################

mkdir -p ${OUTPUT_DIR}

counter=1
while [ $counter -le $NUM_PARTITIONS ]
do
	echo "Starting partition ${counter}"
	echo $(date +%d-%m-%Y" "%H:%M:%S)
	java ${ARGS} -jar java-tool.jar -s ${INPUT_DIR} -t ${OUTPUT_DIR} -pNum ${counter} -pTotal ${NUM_PARTITIONS} -threads ${NUM_THREADS} &>> obfs_output.txt
	killall -s 9 java
	((counter++))
done

echo All done
