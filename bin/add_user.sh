#!/bin/bash
php=$1;
oc_dir=$2;
user_email=$3;
user_uuid=$4;
user_name=$5;
practice_uuid=$6;
export OC_PASS=$user_uuid;
cd $oc_dir;
$php occ user:add --password-from-env --display-name $user_name --email $user_email --group $practice_uuid $user_email;
$php occ user:enable $user_email;
