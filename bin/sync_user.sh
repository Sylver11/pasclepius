#!/bin/bash
php=$1;
oc_dir=$2;
user_email=$3;
cd $oc_dir;
$php occ files:scan $user_email;
