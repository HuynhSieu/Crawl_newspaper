for fold in logs temp
do
    if [ ! -d $fold ]; then mkdir $fold;fi
done

python -m pip install -r requirement.txt
