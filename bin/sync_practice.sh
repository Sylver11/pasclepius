#!/bin/bash
php=$1;
oc_dir=$2;
practice_id=$3;
cd $oc_dir;
$php occ groupfolders:scan $practice_id;
