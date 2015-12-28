#!/bin/sh

# g.mapset PERMANENT --q

for NAME in $(g.list rast patt="fin.res.mod*" mapset="node_0_0")
do
  # echo $NAME
  MAPS=$(cat nodes | sed -e "s/\(.*\)$/$NAME@\1/g" | tr "\n" ",")
  # MAPS=$(cat done | sed -e "s/\(.*\)$/$NAME@\1/g" | tr "\n" ",")
  echo r.patch input=$MAPS output=$NAME --o "&"
done



