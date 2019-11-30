# Using the models specified in model_defs, run each one on the datasets in java_files
# This creates the .arff files to be used in the weka experimenter in the weka_files folder

NUM_MODELS=6

conda activate tf_new

counter=0
while [ $counter -lt $NUM_MODELS ]
do
    echo "RUNNING MODEL ${counter}"
    echo $(date +%H:%M:%S)
    python main.py $counter
    ((counter++))
done
