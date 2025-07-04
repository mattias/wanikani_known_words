# WaniKani Known Words

## Setup
mv .config-sample to .config and add token from WaniKani with the "all_data:read" permission set.

## If on Ubuntu 24+
python -m venv known_words
source known_words/bin/activate
pip install requests

## Otherwise
pip install requests


## Usage
Run with ´python wanikani_known_words.py´
Copy paste the list into Migaku.
