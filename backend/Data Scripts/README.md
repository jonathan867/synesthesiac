Set up fetch-data & Data cleaning:

- always remove whats in the first row -> it's song credits
- then, find all the areas where the header is reinserted and delete those rows
- also delete rows where lyrics are not found
- Also, sometimes there are non-english lyrics. Remove those
- theres random ads in the file: e.g.  See Olivia Rodrigo LiveGet tickets as low as $66 You might also like
    - these are always their own line, so you need to clean and delete these
- remove anything in brackets: e.g. [Chorus]
