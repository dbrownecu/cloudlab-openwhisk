# CloudLab profile for deploying OpenWhisk via Kubernetes

General information for what on CloudLab profiles created via GitHub repo can be found in the example repo [here](https://github.com/emulab/my-profile) or in the CloudLab [manual](https://docs.cloudlab.us/cloudlab-manual.html)

Specifically, the goal of this repo is to create a CloudLab profile that allows for one-click creation of a Kubernetes OpenWhisk deployment.

## User Information

Create a CloudLab experiment using the OpenWhisk profile. It's recommended to use at least 3 nodes for the cluster. It has been testsed on m510, xl170, and rs630 nodes (e.g., various Intel architectures, not ARM, so do not choose an ARM node). 

On each node, a copy of this repo is available at:
```
    /local/repository
```
Installation specific material (which is baked into the CloudLab disk image) is found at:
```
    /home/cloudlab-openwhisk
```
Docker images are store in additional ephemeral cloudlab storage, mounted on each node at:
```
    /mydata
```

To see information on OpenWhisk pods, make sure to specify the namespace as openwhisk. To remove OpenWhisk,
run the following commands:
```
    $ cd /home/cloudlab-openwhisk/openwhisk-deploy-kube
    $ helm uninstall owdev -n openwhisk
    $ kubectl delete namespace openwhisk
```

To start OpenWhisk again, run:
```
    $ cd /home/cloudlab-openwhisk/openwhisk-deploy-kube
    $ helm install owdev ./helm/openwhisk -n openwhisk -f mycluster.yaml
```

The configuration of OpenWhisk deployed by the experiment is found at: ```/home/cloudlab-openwhisk/openwhisk-deploy-kube/mycluster.yaml```, and is 
identical to the one found [here](mycluster.yaml), except populated with the IP of the primary node. The
default OpenWhisk created by this profile is not optimized in any way. 

To upgrade OpenWhisk, such as after modifying the ```mycluster.yaml``` file, run the following helm command:
```
    $ helm upgrade owdev ./helm/openwhisk -n openwhisk -f mycluster.yaml
```

If anything went wrong with the profile, check the log found at on all nodes:
```
    $ /home/cloudlab-openwhisk/start.log
```

## Versioning
Version 1 of this profile is found in the ```v1``` branch.

## Image Creation

The [```image_setup.sh```](image_setup.sh) script is how the image was created from the base CloudLab Ubuntu 20.04 image.

##Couchdb

```
create a directory for the images
untar xtra.tar into the directory: the directory with the images will be the value assigned to FRSH_FILE_PATH

get correct password from couchdb
kubectl get secret frsh-couch-couchdb -o go-template='{{ .data.adminPassword }}' | base64 --decode
get correct ip address from pod listing

helm repo add couchdb https://apache.github.io/couchdb-helm

helm install frsh-couch couchdb/couchdb  --set couchdbConfig.couchdb.uuid=$(curl https://www.uuidgenerator.net/api/version4 2>/dev/null | tr -d -)

export FRSH_IP=`kubectl get service/frsh-couch-svc-couchdb -o jsonpath='{.spec.clusterIP}'`
export FRSH_USR='admin'
export FRSH_PWD=$(kubectl get secret frsh-couch-couchdb -o go-template='{{ .data.adminPassword }}' | base64 --decode)
export FRSH_URL="http://${FRSH_IP}:5984/"
export FRSH_FILE_PATH="/local/repository/xtra"
curl -X POST -H "Content-Type: application/json" http://admin:"$FRSH_PWD"@"$FRSH_IP":5984/_cluster_setup -d '{"action": "finish_cluster"}'
should return "ok":true}
curl -X GET http://admin:"$FRSH_PWD"@"$FRSH_IP":5984/_all_dbs
should return ["_replicator","_users"]


for manual testing
cd /local/repository
git pull
tar -xvf xtra.tar
pip3 install cloudant
python3 load_coachdb.py  (This can fail. just re run it)
to confirm the database can be read:


wsk -i action create procit --docker st00p1d/action-python-v3.6-ai:latest proc_couchdb.py 

wsk -i action invoke --result procit --param url $FRSH_URL --param passwd $FRSH_PWD 

```
{
    "body": "{\"label\": {\"recs_indb\": 101, \"recs_processed\": 101, \"bytes_read\": 14270647, \"elapsed_time\": 2.9134957709975424}}",
    "statusCode": 200
}
```
to create the resized image db:
python3 init_resize.py
curl -X GET http://admin:"$FRSH_PWD"@"$FRSH_IP":5984/_all_dbs
should return
```
["_replicator","_users","frshimg","resizeimg"]

```

wsk -i action create timeit --docker st00p1d/action-python-v3.6-ai:latest  image_proc3.py 

wsk -i action invoke timeit --result --param url $FRSH_URL --param passwd $FRSH_PWD --param count 12

```
{
    "body": "{\"label\": {\"DB_ClientConnect\": 0.010965187000692822, 
              \"db_client\": 0.007685324999329168, \"rec_count\": 0.005786093999631703, 
              \"keys\": 0.011935210000956431, \"iteration 0: db_inst.get\": 0.015108313004020602, \"iteration 0: doc.get_attachment\": 0.013711341998714488, \"iteration 0: write_file\": 0.0006845719981356524, \"write_file_error\": \"wrote: /tmp/freshen_img_066.png\", \"cv2.imread freshen_img_098.png\": 0.0103047200027504, \"cv2.resize\": 0.0002465659999870695, \"cv2.imwrite\": 0.003785564003919717, \"iteration 0: preprocess_image total\": 0.013314342002558988, \"write2db err\": \"OK: wrote 77285 bytes for 1654744094276\", \"iteration 0: write2db\": 0.108606403999147, \"iteration 1: db_inst.get\": 0.016569327002798673, \"iteration 1: doc.get_attachment\": 0.013181676004023757, \"iteration 1: write_file\": 0.00039540000580018386, \"cv2.imread freshen_img_038.png\": 0.00991789999534376, \"iteration 1: preprocess_image total\": 0.01394514099956723, \"iteration 1: write2db\": 0.10390323699539294, \"iteration 2: db_inst.get\": 0.015228385003865696, \"iteration 2: doc.get_attachment\": 0.015813562997209374, \"iteration 2: write_file\": 0.00040297400119015947, \"cv2.imread freshen_img_047.png\": 0.010453524002514314, \"iteration 2: preprocess_image total\": 0.014518866999424063, \"iteration 2: write2db\": 0.1067464489970007, \"iteration 3: db_inst.get\": 0.015283692002412863, \"iteration 3: doc.get_attachment\": 0.014974742000049446, \"iteration 3: write_file\": 0.0004829039971809834, \"cv2.imread freshen_img_076.png\": 0.012376642000162974, \"iteration 3: preprocess_image total\": 0.01616376099991612, \"iteration 3: write2db\": 0.10532858200167539, \"iteration 4: db_inst.get\": 0.01343989500310272, \"iteration 4: doc.get_attachment\": 0.013808689996949397, \"iteration 4: write_file\": 0.00038232900260481983, \"cv2.imread freshen_img_002.png\": 0.01136393699562177, \"iteration 4: preprocess_image total\": 0.014935813996999059, \"iteration 4: write2db\": 0.1129866920018685, \"iteration 5: db_inst.get\": 0.01477986899408279, \"iteration 5: doc.get_attachment\": 0.016606706005404703, \"iteration 5: write_file\": 0.00025664299755590037, \"cv2.imread freshen_img_091.png\": 0.007391516999632586, \"iteration 5: preprocess_image total\": 0.010121885999978986, \"iteration 5: write2db\": 0.11016270900290692, \"iteration 6: db_inst.get\": 0.014465026994002983, \"iteration 6: doc.get_attachment\": 0.013146594996214844, \"iteration 6: write_file\": 0.00026969700411427766, \"cv2.imread freshen_img_030.png\": 0.008062417000473943, \"iteration 6: preprocess_image total\": 0.01148433200432919, \"iteration 6: write2db\": 0.10319145199900959, \"iteration 7: db_inst.get\": 0.013352258996746968, \"iteration 7: doc.get_attachment\": 0.013962932003778405, \"iteration 7: write_file\": 0.00034821300505427644, \"cv2.imread freshen_img_081.png\": 0.010808642997290008, \"iteration 7: preprocess_image total\": 0.013617548000183888, \"iteration 7: write2db\": 0.10901138399640331, \"iteration 8: db_inst.get\": 0.015438587004609872, \"iteration 8: doc.get_attachment\": 0.013789595999696758, \"iteration 8: write_file\": 0.00039293800364248455, \"cv2.imread freshen_img_001.png\": 0.011882644997967873, \"iteration 8: preprocess_image total\": 0.015405327998450957, \"iteration 8: write2db\": 0.10823571700166212, \"iteration 9: db_inst.get\": 0.01512660500156926, \"iteration 9: doc.get_attachment\": 0.014404292996914592, \"iteration 9: write_file\": 0.0003822840008069761, \"cv2.imread freshen_img_008.png\": 0.008312083002238069, \"iteration 9: preprocess_image total\": 0.01183996500185458, \"iteration 9: write2db\": 0.11157377999916207, \"iteration 10: db_inst.get\": 0.0124478799989447, \"iteration 10: doc.get_attachment\": 0.016866145000676624, \"iteration 10: write_file\": 0.00027321199740981683, \"cv2.imread freshen_img_074.png\": 0.007829638001567218, \"iteration 10: preprocess_image total\": 0.011874332994921133, \"iteration 10: write2db\": 0.11199704599857796, \"iteration 11: db_inst.get\": 0.014246596998418681, \"iteration 11: doc.get_attachment\": 0.01335266499518184, \"iteration 11: write_file\": 0.00038972900074440986, \"cv2.imread freshen_img_066.png\": 0.010644027002854273, \"iteration 11: preprocess_image total\": 0.014782313999603502, \"iteration 11: write2db\": 0.10881896800128743, \"total loop time\": 1.8167000220055343}}",
    "statusCode": 0
}

```angular2html



wsk -i action invoke --result procit --param url $FRSH_URL --param passwd $FRSH_PWD --param dbname resizeimg
```
{
    "body": "{\"label\": {\"dbname\": \"resizeimg\", \"recs_indb\": 9, \"recs_processed\": 9, \"bytes_read\": 445069, \"elapsed_time\": 0.27400944100372726}}",
    "statusCode": 200
}

```


Non looped version of code

```

wsk -i action create timesingle --docker st00p1d/action-python-v3.6-ai:latest  image_proc4.py 

wsk -i action invoke timesingle --result --param url $FRSH_URL --param passwd $FRSH_PWD --param count 1

```


to reset the db
curl -X DELETE http://admin:"$FRSH_PWD"@"$FRSH_IP":5984/resizeimg
python3 init_resize.py



Until I get the script wroking: 


python3.7 -m pip install cloudant
python3.7 -m pip install randimage

under bash:
helm repo add couchdb https://apache.github.io/couchdb-helm
helm install frsh-couch couchdb/couchdb  --set couchdbConfig.couchdb.uuid=$(curl https://www.uuidgenerator.net/api/version4 2>/dev/null | tr -d -)
printf "%s: %s\n" "$(date +"%T.%N")" "Couchdb is not ready yet!"
printf "need to run finish_cluster before using the db!"

   ```

