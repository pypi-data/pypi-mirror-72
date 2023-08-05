# Ejana smear

> The package is a part of Electron Ion Collider ESCalate project [(located here)](https://gitlab.com/eic/escalate)


Simple command line interface to eic-smear and jleic-smear particle smearing engines. 

## Make smearing simple:

Smear the file with handbook detector

```bash
ejana_smear beagle_eD.txt
```

Smears the file using BeAST detector, use only 10k events, name output file as my_file.root

```bash
ejana_smear -d beast -n 10000 beagle_eD.txt -o my_file.root 
```

List of all available detector parametrisations:

```bash
ejana_smear -l    # --list
```

[Read the full documentation](https://gitlab.com/eic/escalate/ejana_smear) 