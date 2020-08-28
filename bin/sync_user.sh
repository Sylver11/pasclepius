#!/bin/bash
oc_dir=$1;
user_email=$2;
cd $oc_dir;
php occ files:scan $user_email;
