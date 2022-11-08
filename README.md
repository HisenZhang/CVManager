# CVManager

An CV and experience manager.

Manage your experience like literatures, and CVs are bibliography.

## Features

- Handles "forthcoming" "-present" date-related case
- Filters experience by tags and priority
- Generates in different formats (PDF, HTML, PNG)
- Deploys to multiple destinations
- Supports digital signature

## Run

```bash
python CVManager.py PATH_TO_PROFILE
```

## How Does It Work?

![flowchart](https://i.imgur.com/M8NRPH4.png)

There are three essential input files:

1. Experience database. This yaml database keeps your experience.
2. CV profile. This yaml configures what to include, and where to deploy, etc.
3. CV template. This HTML jinja template defines your CV's look.

The program first renders your CV in html based on inputs, then convert it to PDF and  other formats if specified.

## Directory Structure

Below is an example directory structure.

```plaintext
.
├─asset                     # input directory
│  ├─image
│  ├─key
│  ├─profile                # CV profile
│  │    example.yml
│  │    academic.yml
│  │    industrial.yml
│  └─data.yml               # experience database
│
├─build                     # output directory
│  ├─2022-10-31-example
│  ├─2022-11-01-academic
│  └─2022-11-05-industrial
│
├─script                    # some helpful scrips
│  └─windows
│                
└─theme                     # put templates here
```
