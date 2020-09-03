#!/bin/bash
php=$1;
oc_dir=$2;
practice_name=$3;
practice_uuid=$4;
practice_id=$5;
cd $oc_dir;
$php occ groupfolders:create $practice_name
$php occ groupfolders:group $practice_id $practice_uuid write
