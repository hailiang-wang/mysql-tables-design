#! /bin/bash 
###########################################
#
###########################################

# constants
baseDir=$(cd `dirname "$0"`;pwd)
cwdDir=$PWD
export PYTHONUNBUFFERED=1
export PATH=/opt/miniconda3/envs/venv-py3/bin:$PATH
export TS=$(date +%Y%m%d%H%M%S)
export DATE=`date "+%Y%m%d"`
export DATE_WITH_TIME=`date "+%Y%m%d-%H%M%S"` #add %3N as we want millisecond too
export CSKEFU_ROOT=~/cskefu/cskefu

# functions

# main 
[ -z "${BASH_SOURCE[0]}" -o "${BASH_SOURCE[0]}" = "$0" ] || return
cd $baseDir/..

if [ ! -f .env ]; then
  echo ".env Not Found" `pwd`/.env
  exit 1
fi

source .env

if [ ! -d tmp ]; then
  mkdir tmp
fi

set -x
cp assets/CentralTopic.xmind $OUTPUT_FILENAME_XMIND
python app/parse_tables_to_xmind.py

if [ $? -eq 0 ]; then
  cp $OUTPUT_FILENAME_XMIND $CSKEFU_ROOT/docs/mysql-mindmap.xmind
  echo "Generate file" `pwd`/$OUTPUT_FILENAME_XMIND
else
  echo "Failed"
  exit 1
fi