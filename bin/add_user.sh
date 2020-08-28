#!/bin/bash
oc_dir=$1;
user_email=$2;
user_uuid=$3;
user_name=$4;
practice_uuid=$5;
export OC_PASS=$user_uuid;
cd $oc_dir;
php occ user:add --password-from-env --display-name $user_name --email $user_email --group $practice_uuid $user_email;
php occ user:enable $user_email;
