import json

poet = json.load(
    open('ntuples.json', 'r')
)

miniaod = json.load(
    open('ntuples_nevts.json', 'r')
)

ntuples = {
    "data": {},
    "ttbar": {},
    "wjets": {}
}

def get_factor(process, variation):

    return poet[process][variation]["nevts_total"] / miniaod[process][variation]["number_events"]


def update_dict(process, variation):

    factor = get_factor(process, variation)

    print(
        process, variation, factor
    )
    
    ntuples[process].update(
        {
            variation: {
                "factor": factor
            }
        }
    )


update_dict("data", "nominal")
update_dict("ttbar", "nominal")
update_dict("wjets", "ME_var")

output_file_name = 'ntuples_factors.json'

json.dump(
    ntuples,
    open(output_file_name, 'w'),
    sort_keys=False,
    indent=4
)

print(
    f"Output written to {output_file_name}"
)
