import json
import os

from subprocess import (
    PIPE,
    run
)

ntuples = {
    "data": {},
    "ttbar": {},
    "wjets": {}
}

def get_number_events(recid):
    '''
    Given a recid in the CODP get the number of events.
    This doesn't work for all recids of course.
    '''
    result = run(
        f"cernopendata-client get-metadata --recid {recid}",
        stdout=PIPE,
        stderr=PIPE,
        universal_newlines=True,
        shell=True
    )

    record = json.loads(str(result.stdout))
    number_events = record['distribution']['number_events']

    return number_events
    
def update_dict(process, variation, recids):
    
    number_events = sum([get_number_events(r) for r in recids])
    
    print(
        process, variation, number_events
    )

    
    ntuples[process].update(
        {
            variation: {
                "number_events": number_events
            }
        }
    )

update_dict("data", "nominal", [24132])
update_dict("ttbar", "nominal", [19359])
update_dict("wjets", "ME_var", [19949])

output_file_name = 'ntuples_nevts.json'

json.dump(
    ntuples,
    open(output_file_name, 'w'),
    sort_keys=False,
    indent=4
)

print(
    f"Output written to {output_file_name}"
)