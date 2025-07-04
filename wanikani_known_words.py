import requests
import configparser
import datetime

config = configparser.ConfigParser()
config.read('.config')
api_token = config['wanikani']['api_token']

headers = {
    'Authorization': f'Bearer {api_token}',
    'Wanikani-Revision': '20170710'
}

now = datetime.datetime.now(datetime.timezone.utc)
one_week_ago = now - datetime.timedelta(days=7)

# WaniKani SRS levels: 5 = Guru, 6 = Master, 7 = Enlightened, 8 = Burned
MIN_SRS_STAGE = 5

def get_recent_assignments():
    url = 'https://api.wanikani.com/v2/assignments'
    assignments = []
    params = {
            'updated_after': one_week_ago.replace(microsecond=0).isoformat().replace('+00:00', 'Z'),  # ISO 8601-format
        'subject_type': 'vocabulary,kana_vocabulary',
        'srs_stages': ','.join(map(str, range(MIN_SRS_STAGE, 9)))  # Guru+
    }

    while url:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        assignments += data['data']
        url = data['pages']['next_url']
        params = {}

    return assignments

def get_subjects(subject_ids):
    url = 'https://api.wanikani.com/v2/subjects'
    subjects = {}
    params = {
        'ids': ','.join(map(str, subject_ids))
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()
    for item in data['data']:
        if item['object'] == 'vocabulary':
            subjects[item['id']] = item['data']['characters']
        if item['object'] == 'kana_vocabulary':
            subjects[item['id']] = item['data']['characters']
    return subjects

def main():
    assignments = get_recent_assignments()
    subject_ids = [a['data']['subject_id'] for a in assignments]
    if not subject_ids:
        print("No new words with Guru-status or higher this week.")
        return

    subjects = get_subjects(subject_ids)
    words = list(subjects.values())
    print(','.join(words))

if __name__ == '__main__':
    main()

