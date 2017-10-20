# dataintegrity

A simple python app to check whether two databases contain the same data in all public tables. Created to verify that Montagu db was
 not corrupted when the server overheated.
 
## Usage
 
We compared a backup of the Montagu database at 2am on 6th October (the evening before the server failure) with the current 
database running on production.

Steps:

From your Montagu repository
1. deploy Montagu locally and copy the running database into a new local database using psql utilities
2. run `./backup/cli.py list` to see available backups
3. run `./backup/restore.py [version]` with the desired version (the pre-corruption version)
4. again, copy the running database into a new local database with a different name (e.g. 'montagu_old')

Then, from this repository:

5. check settings are correct in `settings.json`
6. run `./check.py`

Inconsistencies will be printed to the console.
