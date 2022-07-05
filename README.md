# ATS-Flux Specific Instructions

## Getting Started

Running ATS under Flux requires a Flux installation in `/usr/bin/flux` >=0.38.0. 
All TOSS4 and TOSS3 systems at LLNL should provide this.

Flux is controlled in ATS under the `atsflux` binary. In order to pick up this binary
(defined in ats/bin/atsflux.py and controlled by setup.cfg) you will need to reinstall
ATS. It is recommended that you do this in a virtual environment (instructions for LC 
systems provided below):

```
# Load a python 3.8 module, or otherwise put python 3.8 in your path
module load python/3.8.2

# Create a fresh Python 3.8 (or higher) executable to be shared.
python3 -m virtualenv --system-site-packages --python=python3.8 <NEW_ENV_PATH>

# I named my environment "my_ats_env" in my ~/ directory.

# Clone ATS
git clone git@github.com:wihobbs/ATS.git

# Get the flux branch and switch to that branch
git fetch origin flux
git checkout flux

# pip install cloned ATS into fresh shared Python 3.8 (or higher) executable.
<NEW_ENV_PATH>/bin/python3 -m pip install <CLONE_PATH>/
```
For the pip install, you can add the `-e` flag, which will allow you to modify the repo and pip automatically picks up the changes.

## Flux features for ATS users

`atsflux` has several options for user-defined parameters when running an ATS test
suite under Flux.

```
        --nodes= 
          Specify a number of nodes to use, will default to use 3.
        --bank=
          Specify a project bank to charge, will default to use whatever your default bank is.
        --partition=
          Specify either the debug or batch partition, will default to use debug.
 ```
 
 To run on an LC cluster, generate an `test.ats` file and pass it to `atsflux`. For example:

```
(my_ats_env) (base) [hobbs17@ruby966:Kripke]$ atsflux --bank=cbronze test.ats 
INFO: atsflux will use bank cbronze
Executing: salloc --nodes=3 --partition=pdebug --account=cbronze --time=60 srun -N3 -n3 --pty /usr/bin/flux start -o,-S,log-filename=out /g/g20/hobbs17/my_ats_env/bin/ats test.ats
```

## Release

ATS is licensed under the BSD 3-Clause license, (BSD-3-Clause or
https://opensource.org/licenses/BSD-3-Clause).

Refer to [LICENSE](LICENSE)

LLNL-CODE-820679

