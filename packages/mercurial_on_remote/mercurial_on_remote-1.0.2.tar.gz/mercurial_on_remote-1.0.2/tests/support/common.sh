# A few common settings and helpers for tests

WORK_DIR=${WORK_DIR-$CRAMTMP/work}
rm -rf $WORK_DIR

# dummyssh uses this variable (as mount directory)
export WORK_DIR

# To make some outputs consistent
export COLUMNS=80

# To report errors from sth | grep
# - (doesn't work in dash)
# set -o pipefail
# - mispipe would be OK but adds extra quoting
# - so we just use redirect and define standard targets…
OUT=$WORK_DIR/out
ERR=$WORK_DIR/err


