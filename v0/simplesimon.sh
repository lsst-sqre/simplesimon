#!/usr/bin/env bash
# Requires bash 4 or later, because of associative arrays
unset DEBUG # We don't want the loud output
declare -A results # Declare our results hashes
declare -A wfmap
delay=10 # seconds between iterations
# Determine WF API address from Hub namespace and prefix.
#  The WF API runs in the same NS as the Hub, and its name
#   will be the hub prefix plus wf-api.  It listens on port
#   8080 and does not do TLS.
extracted=$(echo $JUPYTERHUB_API_URL | cut -d '/' -f 3)
ns=$(echo ${extracted} | cut -d '.' -f 2 | cut -d ':' -f 1)
prefix=$(echo ${extracted} | cut -d '.' -f 1 | sed -e 's/-hub//')
wf="http://${prefix}-wf-api.${ns}:8080"
echo "Workflow API URL is ${wf}."
# Create the workflow input JSON documents
./make_drivers.py
img=$(echo ${JUPYTER_IMAGE_SPEC} | cut -d ':' -f 2)
run="run_${img}_wf.sh"
# Execute the test-runner harness.
echo "Executing ${run}."
./${run} 2>/dev/null
# Initialize the workflow map and results hashes
for i in *{img}*.log; do
    tname=$(basename $i .log)
    w=$(cat $i | jq -r .name)
    wfmap[$tname]="${w}"
    results[$tname]="unknown"
done
# Loop until we have results from each of our workflows
while : ; do
    waitfor=""
    for tname in "${!wfmap[@]}"; do
    w=${wfmap[$tname]}
    r=${results[$tname]}
    if [ "${r}" == "Succeeded" ] || [ "${r}" == "Failed" ] \
        || [ "${r}" == "Error" ]; then
        # We have a terminal status for this workflow already.
        continue
    fi
    echo "Checking progress of workflow ${w} [${tname}]."
    ph=$(workflow-api-client -u $wf -w $w inspect 2>/dev/null | \
        jq -r .status.phase)
    echo "Phase for ${tname} is '${ph}'."
    results[$tname]="${ph}"
    # If we're still waiting, record who we're waiting for.
    if [ -z "${ph}" ] || [ "${ph}" == "Running" ]; then
        if [ -z "${waitfor}" ]; then
        waitfor="${tname}"
        else
        waitfor="${waitfor} ${tname}"
        fi
    fi
    done
    if [ -z "${waitfor}" ]; then
    break # If we have nothing left to wait for, exit the while loop
    fi
    echo "Waiting ${delay}s for [${waitfor}]."
    sleep ${delay}
done
# All our workflows have now completed.  Assemble the status.
succeeded=""
failed=""
for tname in "${!results[@]}"; do
    r=${results[${tname}]}
    if [ "${r}" == "Failed" ] || [ "${r}" == "Error" ]; then
    w=${wfmap[${tname}]}
    echo "Extracting failure for workflow ${w} [${tname}]."
    workflow-api-client -u $wf -w $w logs 2>/dev/null | \
        jq -r .[0].logs > ${tname}.failure
    if [ -z "${failed}" ]; then
        failed="${tname}"
    else
        failed="${failed} ${tname}"
    fi
    elif [ "${r}" == "Succeeded" ]; then
    if [ -z "${succeeded}" ]; then
        succeeded="${tname}"
    else
        succeeded="${succeeded} ${tname}"
    fi
    else
    echo "Unknown result for ${tname}: ${r}."
    fi
done
# Report that status
if [ -n "${failed}" ]; then
    echo "FAILED TESTS: ${failed}."
fi
if [ -n "${succeeded}" ]; then
    echo "SUCCEEDED: ${succeeded}."
fi
