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
get crorect ip address from pod listing

curl -X POST -H "Content-Type: application/json" http://admin:"$CORRECT_PASSWORD"@"$CORRECT_IP_ADDR":5984/_cluster_setup -d '{"action": "finish_cluster"}'
curl -X GET http://admin:"$CORRECT_PASSWORD"@"$CORRECT_IP_ADDRESS":5984/_all_dbs
should return ["_replicator","_users"]

export FRSH_USR='admin'
export FRSH_PWD=$(kubectl get secret frsh-couch-couchdb -o go-template='{{ .data.adminPassword }}' | base64 --decode)
export FRSH_URL='http://ip_addr_of_server:5984/'
export FRSH_FILE_PATH='Directory containing the contents of xtra.tar'

or for tsch
setenv FRSH_USR 'admin'
setenv FRSH_PWD $(kubectl get secret frsh-couch-couchdb -o go-template='{{ .data.adminPassword }}' | base64 --decode)
setenv FRSH_URL 'http://ip_addr_of_server:5984/'
setenv FRSH_FILE_PATH DIRECTORY_OF_IMAGES_FOR_DB

python3 load_coachdb.py

Until I get the script wroking: 

python3.7 -m pip install tensorflow
python3.7 -m pip install cloudant

helm repo add couchdb https://apache.github.io/couchdb-helm
helm install frsh-couch couchdb/couchdb  --set couchdbConfig.couchdb.uuid=$(curl https://www.uuidgenerator.net/api/version4 2>/dev/null | tr -d -)
printf "%s: %s\n" "$(date +"%T.%N")" "Couchdb is not ready yet!"
printf "need to run finish_cluster before using the db!"

   ```

