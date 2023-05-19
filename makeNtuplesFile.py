#!/usr/bin/env python
# coding: utf-8

# In[ ]:


'''
Produce the ntuples.json file needed for the
analysis. 

NOTE: This script needs to be run in an environment where
EOS is installed (lxplus or SWAN will work)

'''

import json
import os
import uproot
import yaml

from subprocess import (
    PIPE,
    run
)

eos_env = 'root://eospublic.cern.ch'
os.environ["EOS_MGM_URL"] = eos_env

poet_path = '/eos/opendata/cms/upload/POET/23-Jul-22/'

contents = run(
    f"xrdfs {eos_env} ls {poet_path}",
    stdout=PIPE,
    stderr=PIPE,
    universal_newlines=True,
    shell=True
)

contents = contents.stdout.split('\n')[:-1]


# In[ ]:


# These are the dirs which contain the files we want
data_dirs = [d for d in contents if '_flat' in d and '.root' not in d]

# These dirs contain the metadata which we can query as a check (re: number of events)
# We will query the root files directly later to determine number of events
metadata_dirs = [d for d in contents if not '_flat' in d and '.root' not in d]


# In[ ]:

#RunIIFall15MiniAODv2_TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8
# See what's in the metadata yaml files
metadata = run(
    f"xrdfs {eos_env} cat {poet_path}/RunIIFall15MiniAODv2_TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/metadata.yaml",
    stdout=PIPE,
    stderr=PIPE,
    universal_newlines=True,
    shell=True
)

md = yaml.safe_load(
    metadata.stdout
)


# In[ ]:


# How to get the number of events in the miniAOD?

with uproot.open(
                'root://eospublic.cern.ch//eos/opendata/cms/mc/RunIIFall15MiniAODv2/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/40000/003BD8A4-C1CB-E511-A84A-001E67A3E95D.root'
) as f:
    print(
        f.keys()
    )
    print(
        f'{f["Events"].num_entries} events'
    )


# In[ ]:


ntuples = {
    "data": {},
    "ttbar": {},
    "wjets": {}
}


# In[ ]:


def get_files(process_dir):
    
    file_names = []
    
    for d in process_dir:
    
        files = run(
                    f"xrdfs {eos_env} ls {poet_path}{d}",
                    stdout=PIPE,
                    stderr=PIPE,
                    universal_newlines=True,
                    shell=True
                )
    
        fns = files.stdout.split('\n')[:-1]
        file_names += [f"{eos_env}/{fn}" for fn in fns]
    
    return file_names


def num_events_list(files):
    
    num_events = []
    
    for i, file_name in enumerate(files):
        
        with uproot.open(file_name) as f:
            
            num_events.append(
                f["events"].num_entries
            )
            
    return num_events


def update_dict(process, variation, process_dir):
    
        print(
            process_dir
        )
    
        files = get_files(process_dir)
        nevts_list = num_events_list(files)
    
        ntuples[process].update(
            {
                variation: {
                "files": [{"path": f, "nevts": n} for f, n in zip(files, nevts_list)],
                "nevts_total": sum(nevts_list),
            }
        }
        
    )


# In[ ]:


update_dict(
    "data", "nominal", 
    [
        "Run2015D_DoubleEG_flat"
    ]
)

update_dict("ttbar", "nominal", ["SMS-T1tttt_mGluino-1200_mLSP-800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_flat"])

update_dict("wjets", "ME_var", ["RunIIFall15MiniAODv2_TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_flat"])


# In[ ]:


output_file_name = 'ntuples.json'

json.dump(
    ntuples,
    open(output_file_name, 'w'),
    sort_keys=False,
    indent=4
)

print(
    f"Output written to {output_file_name}"
)


# In[ ]:
