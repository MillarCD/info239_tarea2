#!bin/bash

names=(diego python natalia qwerty 123457 juan pedro)

clientes=${1?Error: debe ejecutar bash prog.sh <n>}

if [[ $clientes -gt ${#names[@]} ]]
then
  echo "n debe ser menor que ${#names[@]}"
  exit
fi

function ejecClient() {
  python main.py $1
}

for ((i=0;i<${#names[@]};i++))
do

  ejecClient ${names[i]} &

done

wait

