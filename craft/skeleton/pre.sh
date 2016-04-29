#!/bin/bash
#
# Pre processing script run just before a deployment occurs but after a `juju bootstrap`

. /usr/share/conjure-up/hooklib/common.sh

debug {{spell}} "Running pre-exec hook"

exposeResult "Completed pre processing" 0 "true"
