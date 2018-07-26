import os
import requests
import argparse
from datetime import datetime
from time import sleep


class BackupError(Exception):
    pass


def request(method, endpoint, **kwargs):
    response = session.request(method, 'https://api.github.com' + endpoint, **kwargs)
    if not 200 <= response.status_code <= 299:
        raise BackupError('%s on %s got status %s: %s' % (method, endpoint, response.status_code, response.content))

    return response

session = requests.Session()
session.headers['Accept'] = 'application/vnd.github.wyandotte-preview+json'
repos = [
    'EdinburghGenomics/' + r
    for r in ('Analysis-Driver', 'Reporting-App', 'EGCG-Project-Management', 'EGCG-Core', 'Fastq-Filterer')
]


def main():
    a = argparse.ArgumentParser()
    a.add_argument(
        'key_file',
        help="""Path to a single-line file containing GitHub API credentials in the format
                'username:personal_access_token'. The access token requires the scope 'admin:org'."""
    )
    a.add_argument('--dest', help='Directory to save archives to (defaults to working dir)', default=os.getcwd())
    a.add_argument('--quiet', dest='stdout', action='store_false')
    args = a.parse_args()

    if args.stdout:
        log = print
    else:
        def log(msg):
            pass

    with open(args.key_file, 'r') as f:
        username, token = f.readline().rstrip('\n').split(':')
        session.auth = requests.auth.HTTPBasicAuth(username, token)

    log('Initiating migration')
    migration_id = request('POST', '/orgs/EdinburghGenomics/migrations', json={'repositories': repos}).json()['id']
    log('Waiting for new migration %s to finish' % migration_id)
    while True:
        sleep(10)
        status = request('GET', '/orgs/EdinburghGenomics/migrations/%s' % migration_id).json()['state']
        if status == 'exported':
            break
        elif status in ('exporting', 'pending'):
            pass
        else:
            raise BackupError('Got status %s' % status)

    log('Downloading migration archive')
    archive = request('GET', '/orgs/EdinburghGenomics/migrations/%s/archive' % migration_id)
    tar_file = 'EdinburghGenomics_archive_%s.tar.gz' % datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    with open(os.path.join(args.dest, tar_file), 'wb') as f:
        f.write(archive.content)

    log('Cleaning up server-side archive')
    request('DELETE', '/orgs/EdinburghGenomics/migrations/%s/archive' % migration_id)

    log('Done')


if __name__ == '__main__':
    main()
