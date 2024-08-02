# Replication package of our study

We hereby describe the structure of our project and provide instructions to replicate our study.

## Analyze results 

tbd

## bytecode folder

This folder contains the bytecode in .hex of each Smart Contact of our sample of interest, organized by original source.

## csvs folder

This folder contains the csv dataset used in our study

## gpt folder

This folder contains the script to call ChatGPT APIs

## improve_parsing_script folder

this folder contains script to parse .log result of smartbugs when using oyente and securify

## scripts

### calculate_metrics

this script reports the considered metrics values

### compile

this script compiles smart contracts which do not have addresses

### get_bytecode

this script leverages ehterscan API to get the bytecode of a given smart contract

### main

this script allows you to select what do you want to carry on, such as Compile dataset files, Parse analysis results, 
compare tool considering or not arithmetic issues

### parse_vulnerability

This script enables the parsing of smartbugs tools' results

### vulnerability_mapping

This script allows to find new vulnerabilities which are not previously mapped to DASP categories

## vulenrability_log

This csv shows the vulnerabilities found by each tool, for each contract, alongside the DASP vulenrabilties that the 
tools found
