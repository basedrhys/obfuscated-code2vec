NUM_MODELS=5

conda activate tf_new

counter=4
while [ $counter -lt $NUM_MODELS ]
do
    echo "RUNNING MODEL ${counter}"
    python main.py $counter
    ((counter++))
done
