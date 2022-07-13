pcpath=%1
patname=%2
curdir=pwd

if [ -z "$pcpath" ]; then
    echo "Please provide a path to the pcreate folder"
    exit 1
fi

if [ -z "$patname" ]; then
    patname="default"
fi

cd $pcpath
python3 main.py $patname ai $curdir/presets.json

cd $curdir
python3 main.py $patname