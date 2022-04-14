#!/usr/bin/bash
python3.7 -m pip install tensorflow
python3.7 -m pip install cloudant

helm repo add couchdb https://apache.github.io/couchdb-helm
helm install frsh-couch couchdb/couchdb  --set couchdbConfig.couchdb.uuid=$(curl https://www.uuidgenerator.net/api/version4 2>/dev/null | tr -d -)
printf "%s: %s\n" "$(date +"%T.%N")" "Couchdb is not ready yet!"
printf "need to run finish_cluster before using the db!"
mkdir ~/xtra_data
cp /local/repository/xtar.tar ~/xtra_data
tar -xvf ~/xtra_data
