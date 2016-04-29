#!/bin/bash
#
# This is the post processing script, it is run continuously after deployment finishes. It is run
# in a loop until the last exposeResult call is made. This is done to make sure we can poll for
# services that may not be completely ready yet.

. /usr/share/conjure-up/hooklib/common.sh

exposeResult "Done post.sh" 0 "true"
