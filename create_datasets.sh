NUM_MODELS=2

conda activate tf_new

counter=0
while [ $counter -lt $NUM_MODELS ]
do
    echo "RUNNING MODEL ${counter}"
    python main.py $counter
    ((counter++))
done