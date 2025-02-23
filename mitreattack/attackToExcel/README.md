# ATT&CK To Excel

This folder contains a module for converting [ATT&CK STIX data](https://github.com/mitre/cti) to Excel spreadsheets. It also provides a means to access ATT&CK data as [Pandas](https://pandas.pydata.org/) DataFrames for data analysis.

## Usage
### Command Line
Print full usage instructions:
```
python3 attackToExcel.py -h
```

Example execution:
```
python3 attackToExcel.py
```

Build a excel files corresponding to a specific domain and version of ATT&CK:
```
python3 attackToExcel -domain mobile-attack -version v5.0
```

### Module 

Example execution targeting a specific domain and version: 
```python
import mitreattack.attackToExcel.attackToExcel as attackToExcel

attackToExcel.export("mobile-attack", "v5.0", "/path/to/export/folder")
```

## Interfaces

### attackToExcel
attackToExcel provides the means by which to convert/extract the ATT&CK STIX data to Excel spreadsheets. A brief 
overview of the available methods follows.

| method name | arguments | usage |
|:------------|:----------|:------|
|get_stix_data|`domain`: the domain of ATT&CK to fetch data from <br> `version`: optional parameter indicating which version to fetch data from (such as "v8.1"). If omitted retrieves the most recent version of ATT&CK. <br>`remote`: optional parameter that provides a URL of a remote ATT&CK Workbench instance to grab data from.| Retrieves the ATT&CK STIX data for the specified version and returns it as a MemoryStore object|
|build_dataframes| `src`: MemoryStore or other stix2 DataSource object holding domain data<br> `domain`: domain of ATT&CK that `src` corresponds to| Builds a Pandas DataFrame collection as a dictionary, with keys for each type, based on the ATT&CK data provided|
|write_excel| `dataframes`: pandas DataFrame dictionary (generated by build_dataframes) <br>  `domain`: domain of ATT&CK that `dataframes` corresponds to <br> `version`: optional parameter indicating which version of ATT&CK is in use <br> `outputDir`: optional parameter specifying output directory| Writes out DataFrame based ATT&CK data to excel files|
|export| `domain`: the domain of ATT&CK to download <br> `version`: optional parameter specifying which version of ATT&CK to download <br> `outputDir`: optional parameter specifying output directory| Downloads ATT&CK data from MITRE/CTI and exports it to Excel spreadsheets | 

### stixToDf
stixToDf provides various methods to process and manipulate the STIX data in order to create [Pandas](https://pandas.pydata.org/) DataFrames for 
processing. A brief overview of these methods follows.

| method name | arguments | usage |
|:------------|:----------|:------|
|techniquesToDf|`src`: MemoryStore or other stix2 DataSource object holding domain data<br> `domain`: domain of ATT&CK that `src` corresponds to | Parses STIX techniques from the provided data and returns corresponding Pandas DataFrames.|
|tacticsToDf|`src`: MemoryStore or other stix2 DataSource object holding domain data<br> `domain`: domain of ATT&CK that `src` corresponds to | Parses STIX tactics from the provided data and returns corresponding Pandas DataFrames.|
|softwareToDf|`src`: MemoryStore or other stix2 DataSource object holding domain data<br> `domain`: domain of ATT&CK that `src` corresponds to | Parses STIX software from the provided data and returns corresponding Pandas DataFrames.|
|groupsToDf|`src`: MemoryStore or other stix2 DataSource object holding domain data<br> `domain`: domain of ATT&CK that `src` corresponds to | Parses STIX groups from the provided data and returns corresponding Pandas DataFrames.|
|mitigationsToDf|`src`: MemoryStore or other stix2 DataSource object holding domain data<br> `domain`: domain of ATT&CK that `src` corresponds to | Parses STIX mitigations from the provided data and returns corresponding Pandas DataFrames.|
|relationshipsToDf|`src`: MemoryStore or other stix2 DataSource object holding domain data<br> `domain`: domain of ATT&CK that `src` corresponds to | Parses STIX relationships from the provided data and returns corresponding Pandas DataFrames.|
|matricesToDf|`src`: MemoryStore or other stix2 DataSource object holding domain data<br> `domain`: domain of ATT&CK that `src` corresponds to | Parses STIX matrices from the provided data and returns a parsed matrix structure of the form `[{matrix, name, description, merge, border}, ...]`|

## Spreadsheet format

The Excel representation of the ATT&CK dataset includes both master spreadsheets, containing all object types, and individual spreadsheets for each object type. The individual type spreadsheets break out relationships (e.g procedure examples connecting groups to techniques) into separate sheets by relationship type, while the master spreadsheet includes all relationship types in a single sheet. Otherwise, the representation is identical.

A citations sheet can be used to look up the in-text citations which appear in some fields. For domains that include multiple matrices, such as Mobile ATT&CK, each matrix gets its own named sheet. Unlike the STIX dataset, objects that have been revoked or deprecated are not included in the spreadsheets.

## Accessing the Pandas DataFrames

Internally, attackToExcel stores the parsed STIX data as [Pandas](https://pandas.pydata.org/) DataFrames. These can be retrieved for use in data analysis. 

Example of accessing [Pandas](https://pandas.pydata.org/) DataFrames:
```python
import mitreattack.attackToExcel.attackToExcel as attackToExcel
import mitreattack.attackToExcel.stixToDf as stixToDf

# download and parse ATT&CK STIX data
attackdata = attackToExcel.get_stix_data("enterprise-attack")
techniques_data = stixToDf.techniquesToDf(attackdata, "enterprise-attack")

# show T1102 and sub-techniques of T1102
techniques_df = techniques_data["techniques"]
print(techniques_df[techniques_df["ID"].str.contains("T1102")]["name"])
# 512                                 Web Service
# 38     Web Service: Bidirectional Communication
# 121             Web Service: Dead Drop Resolver
# 323          Web Service: One-Way Communication
# Name: name, dtype: object

# show citation data for LOLBAS Wmic reference
citations_df = techniques_data["citations"]
print(citations_df[citations_df["reference"].str.contains("LOLBAS Wmic")])
#         reference                                           citation                                                url
# 1010  LOLBAS Wmic  LOLBAS. (n.d.). Wmic.exe. Retrieved July 31, 2...  https://lolbas-project.github.io/lolbas/Binari...
```