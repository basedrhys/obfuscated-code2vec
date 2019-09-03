NUM_MODELS=6

conda activate tf_new

counter=0
while [ $counter -lt $NUM_MODELS ]
do
    echo "RUNNING MODEL ${counter}"
    echo $(date +%H:%M:%S)
    python main.py $counter &>> /Scratch/git/dataset_output.txt
    ((counter++))
done
