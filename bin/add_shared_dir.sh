#!/bin/bash
php=$1;
oc_dir=$2;
practice_name=$3;
cd $oc_dir;
$php occ groupfolders:create "$practice_name"
