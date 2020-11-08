#!/bin/bash
php=$1;
oc_dir=$2;
practice_uuid=$3;
folder_id=$4;
cd $oc_dir;
$php occ groupfolders:group $folder_id $practice_uuid write
$php occ groupfolders:scan $folder_id
