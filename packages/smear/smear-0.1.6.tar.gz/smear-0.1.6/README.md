# Smear command
Simple command line interface to eic-smear and jleic-smear


### Full CLI help

**Usage:** 

``` bash
  ejana_smear <flags> [input file]   # smears the input file
  ejana_smear -l                     # list of available detectors
```


**Examples:** 

```bash
  ejana_smear beagle_eD.txt                     # smear the file with handbook detector
  ejana_smear beagle_eD.txt -o my_file.root     # smears the file and set output file name  
  ejana_smear -d beast -n 10000 beagle_eD.txt   # uses beast detector, smears only 10k events
```

**main flags:**

| Flag             | Description |
|------------------|-------------|
| -l / --list      | Show all detectors and versions|
| -d / --detector  | Detector parametrisation. Handbook is default. Run -l/--list flag to see all options
| -n / --nevents   | Number of events to process |
| -s / --nskip     | Number of events to skip |    
| -o / --output    | Output file name |    
| -j / --threads   | Number of threads. Set 'auto' for max. Default is 1 |  
| -h / --help      | Show help |



**Advanced flags:**

| Flag | Description |
|------|-------------|
| t / --input-type |   Input file type. Select from: beagle, hepmc2, lund, eic_pythia6, g4e, auto |
| a / --analysis   |   Comma separated additional analysis list |
| --explain        |    Explain all configurations, but don't run smearing |


**Number of events:**

One can set a number of events by -n(--nevents) and -s(--nskip) flags. Flag -n also support ranges:
```  
    -n 100        : process 100 events
    -s 100 -n 50  : skip first 100 events, and process 50 events
    -s 100        : skip first 100 events and process the rest
```

**Known file formats:**

Applies to -t / --input-type. Options: beagle, hepmc2, lund, eic_pythia6, g4e, auto

**Detector names and versions**

   | Engine | Name         | Version and Link |
   |--------|--------------|------------------|
   | ES     | handbook     | [HandBook v1.0.4](https://gitlab.com/eic/escalate/ejana/blob/master/src/plugins/reco/eic_smear/ESDetectorHandBook_v1_0_4.cc) |
   | ES     | beast        | [BeAST v1.0.4](https://gitlab.com/eic/escalate/ejana/blob/master/src/plugins/reco/eic_smear/ESDetectorBeAST_v1_0_4.cc) |
   | ES     | ephenix      | [ePHENIX v1.0.4](https://gitlab.com/eic/escalate/ejana/blob/master/src/plugins/reco/eic_smear/ESDetectorEPHENIX_v1_0_4.cc) |
   | ES     | zeus         | [DetectorZeus v1.0.0](https://gitlab.com/eic/escalate/ejana/blob/master/src/plugins/reco/eic_smear/ESDetectorZeus_v1_0_0.cc) |
   | YF     | yfhandbook   | [Handbook v1.0.0](https://gitlab.com/eic/escalate/ejana/blob/master/src/plugins/reco/eic_smear/YFDetectorHandbook_v1_0_0.cc) |
   | YF     | jleic        | [Jleic v1.0.2](https://gitlab.com/eic/escalate/ejana/blob/master/src/plugins/reco/eic_smear/YFDetectorJleic_v1_0_2.cc) |
   | YF     | jleic-v1.0.1 | [Jleic v1.0.1](https://gitlab.com/eic/escalate/ejana/blob/master/src/plugins/reco/eic_smear/YFDetectorJleic_v1_0_1.cc) |
   >    ES - eic-smear, YF - Yulia Furletova
