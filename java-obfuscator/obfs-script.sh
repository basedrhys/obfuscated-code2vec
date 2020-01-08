#!/usr/bin/env bash
###########################################################
INPUT_DIR="/path/to/your/java/files"
OUTPUT_DIR="/path/to/where/you/want/obfuscated/files"
OBFS_TYPE="-r" # -r for random, leave as empty string for type obfuscation
NUM_PARTITIONS=1 # You may need to increase partitions if obfuscating millions of files (e.g. java-large)
NUM_THREADS=13
ARGS=""
###########################################################

mkdir -p ${OUTPUT_DIR}

counter=1
while [ $counter -le $NUM_PARTITIONS ]
do
	echo "Starting partition ${counter}"
	echo $(date +%d-%m-%Y" "%H:%M:%S)
	java ${ARGS} -jar java-tool.jar \
		-s ${INPUT_DIR} \
		-t ${OUTPUT_DIR} \
		-pNum ${counter} \
		-pTotal ${NUM_PARTITIONS} \
		-threads ${NUM_THREADS} \
		${OBFS_TYPE}

	killall -s 9 java 
	((counter++))
done

echo "All done"
