#!/bin/bash

# This script is for Nagios monitoring of Kafka queues via SNMP.
# It's good example how to write script with named arguments

# for multiple results
function get_rtrn(){
    echo "$1"|cut --delimiter=, -f "$2"
}

function usage(){
    read -r -d '' USAGE << EOM
Usage: bash $0 --group 'group_name' --zookeeper 'zookeeper_nodes' --warning numeric --critical numeric -g OID
       bash $0 --group 'some-rules-engine' --zookeeper '1.2.3.4:2181, 5.6.7.8:2181, 9.10.11.12:2181/events' --warning 5000 --critical 10000 -g .1.2.3.4.5.6.7
EOM
    echo "$USAGE"
}

function output(){
    echo "$OID"
    echo string
}

if [ "$#" == 0 ]; then
    usage
    exit 2
fi

# Parse arguments
while [[ $# -gt 0 ]]
do
    key="$1"

    case $key in
        --group)
            GROUP="$2"
            shift # past argument
        ;;
        --zookeeper)
            ZOOKEEPER="$2"
            shift # past argument
        ;;
        --warning)
            WARNING="$2"
            shift # past argument
        ;;
        --critical)
            CRITICAL="$2"
            shift # past argument
        ;;
        -g)
            OID="$2"
            shift # past argument
        ;;
        -*)
            echo "Unknown option: $1" >&2
            usage
            exit 2
        ;;
        *)
            echo "Script doesn't take non options arguments: $1" >&2
            usage
            exit 2
        ;;
    esac
    shift # past argument or value
done

# Validate settings
if [ -z "$ZOOKEEPER" ]; then
    echo "No --zookeeper argument supplied"
    usage
    exit 2
elif [ -z "$GROUP" ]; then
    echo "No --group argument supplied"
    usage
    exit 2
elif [ -z "$WARNING" ]; then
    echo "No --warning argument supplied"
    usage
    exit 2
elif [ -z "$CRITICAL" ]; then
    echo "No --critical argument supplied"
    usage
    exit 2
elif [ "$WARNING" -ge "$CRITICAL" ]; then
    echo "--critical value should be bigger than --warning"
    usage
    exit 2
elif [ -z "$OID" ]; then
    echo "No -g (OID) argument supplied"
    usage
    exit 2
fi

# awk sums columns
SUM_COLUMN='
$1 == GROUP {
    group = $1
    offset = $4
    log_size = $5
    lag = $6

    sum_offset += offset
    sum_log_size += log_size
    sum_lag += lag
}

END {
    print sum_offset","sum_log_size","sum_lag
}
'

cd "$(dirname "$0")" || exit 2

# function call
# https://quantifind.com/KafkaOffsetMonitor/
JAVA_OUTPUT="$(java -cp ../lib/KafkaOffsetMonitor-assembly-0.2.1.jar \
              com.quantifind.kafka.offsetapp.OffsetGetterApp \
              --group "$GROUP" \
              --zk "$ZOOKEEPER" 2> /dev/null | \
              awk -v GROUP="$GROUP" "$SUM_COLUMN")"

# get parts of result
SUM_OFFSET="$(get_rtrn "$JAVA_OUTPUT" 1)"
SUM_LOG_SIZE="$(get_rtrn "$JAVA_OUTPUT" 2)"
SUM_LAG="$(get_rtrn "$JAVA_OUTPUT" 3)"

PERFORMANCE_OUTPUT="sumLag is $SUM_LAG | sumOffset=$SUM_OFFSET sumLogSize=$SUM_LOG_SIZE sumLag=$SUM_LAG"

# Nagios output
if [ -z "$SUM_OFFSET" ] || [ -z "$SUM_LOG_SIZE" ] || [ -z "$SUM_LAG" ];
then
    output
    echo "3;UNKNOWN-check that Kafka is configured"
    exit 3
elif [ "$SUM_LAG" -lt "$WARNING" ]
then
    output
    echo "0;OK-$PERFORMANCE_OUTPUT"
    exit 0
elif [ "$SUM_LAG" -ge "$WARNING" ] && [ "$SUM_LAG" -le "$CRITICAL" ]
then
    output
    echo "1;WARNING-$PERFORMANCE_OUTPUT"
    exit 1
elif [ "$SUM_LAG" -gt "$CRITICAL" ]
then
    output
    echo "2;CRITICAL-$PERFORMANCE_OUTPUT"
    exit 2
else
    echo "3;UNKNOWN-check script work"
    exit 3
fi
