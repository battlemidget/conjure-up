#!/bin/bash
#
# This is the post-bootstrap processing script. It is run directly after `juju bootstrap`

. /usr/share/conjure-up/hooklib/common.sh

debug {{spell}} "Running post-bootstrap for a {{spell}} install"

exposeResult "Post bootstrap complete" 0 "true"
