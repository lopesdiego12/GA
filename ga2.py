import argparse
from apiclient.discovery import build
from oauth2client.client import SignedJwtAssertionCredentials
import httplib2
from oauth2client import client
from oauth2client import file
from oauth2client import tools
import OpenSSL

def get_service(api_name, api_version, scope, key_file_location,
                service_account_email):

  f = open(key_file_location, 'rb')
  key = f.read()  
  f.close()

  credentials = SignedJwtAssertionCredentials(service_account_email, key,
    scope=scope)

  http = credentials.authorize(httplib2.Http())

  # Build the service object.
  service = build(api_name, api_version, http=http)

  return service


def get_first_profile_id(service):
  # Use the Analytics service object to get the first profile id.

  # Get a list of all Google Analytics accounts for this user
  accounts = service.management().accounts().list().execute()

  if accounts.get('items'):
    # Get the first Google Analytics account.
    account = accounts.get('items')[0].get('id')

    # Get a list of all the properties for the first account.
    properties = service.management().webproperties().list(
        accountId=account).execute()

    if properties.get('items'):
      # Get the first property id.
      property = properties.get('items')[0].get('id')

      # Get a list of all views (profiles) for the first property.
      profiles = service.management().profiles().list(
          accountId=account,
          webPropertyId=property).execute()

      if profiles.get('items'):
        # return the first view (profile) id.
        return profiles.get('items')[0].get('id')

  return None

def get_results(service, profile_id):
  return service.data().ga().get(
      ids='ga:' + profile_id,
      start_date='2019-08-01',
      end_date='2019-08-01',
      dimensions= 'ga:dimension1, ga:sourceMedium',
	  metrics='ga:sessions').execute()

def get_realtime_users(service, profile_id):
    return service.data().realtime().get(
        ids='ga:' + profile_id,
        metrics='rt:activeUsers',
        dimensions='rt:medium').execute()

def print_results(results):
  """Prints out the results.
  This prints out the profile name, the column headers, and all the rows of
  data.
  Args:
    results: The response returned from the Core Reporting API.
  """

  print()
  print('Profile Name: %s' % results.get('profileInfo').get('profileName'))
  print()

  # Print header.
  output = []
  for header in results.get('columnHeaders'):
    output.append('%30s' % header.get('name'))
  print(''.join(output))

  # Print data table.
  if results.get('rows', []):
    for row in results.get('rows'):
      output = []
      for cell in row:
        output.append('%30s' % cell)
      print(''.join(output))

  else:
    print('No Rows Found')

def print_report_info(results):
  """Prints general information about this report.
  Args:
    results: The response returned from the Core Reporting API.
  """

  print('Report Infos:')
  print('Contains Sampled Data = %s' % results.get('containsSampledData'))
  print('Kind                  = %s' % results.get('kind'))
  print('ID                    = %s' % results.get('id'))
  print('Self Link             = %s' % results.get('selfLink'))

def print_pagination_info(results):
  """Prints common pagination details.
  Args:
    results: The response returned from the Core Reporting API.
  """

  print('Pagination Infos:')
  print('Items per page = %s' % results.get('itemsPerPage'))
  print('Total Results  = %s' % results.get('totalResults'))

  # These only have values if other result pages exist.
  if results.get('previousLink'):
    print('Previous Link  = %s' % results.get('previousLink'))
  if results.get('nextLink'):
    print('Next Link      = %s' % results.get('nextLink'))
  print()


def print_profile_info(results):
  """Prints information about the profile.
  Args:
    results: The response returned from the Core Reporting API.
  """

  print('Profile Infos:')
  info = results.get('profileInfo')
  print()


def print_query(results):
  """The query returns the original report query as a dict.
  Args:
    results: The response returned from the Core Reporting API.
  """

  print('Query Parameters:')
  query = results.get('query')
  for key, value in query.iteritems():
    print('%s = %s' % (key, value))
  print()


def print_column_headers(results):
  """Prints the information for each column.
  The main data from the API is returned as rows of data. The column
  headers describe the names and types of each column in rows.
  Args:
    results: The response returned from the Core Reporting API.
  """

  print('Column Headers:')
  headers = results.get('columnHeaders')
  for header in headers:
    # Print Dimension or Metric name.
    print('\t%s name:    = %s' % (header.get('columnType').title(),
                                  header.get('name')))
    print('\tColumn Type = %s' % header.get('columnType'))
    print('\tData Type   = %s' % header.get('dataType'))
    print()


def print_totals_for_all_results(results):
  """Prints the total metric value for all pages the query matched.
  Args:
    results: The response returned from the Core Reporting API.
  """

  print('Total Metrics For All Results:')
  print('This query returned %s rows.' % len(results.get('rows')))
  print(('But the query matched %s total results.' %
         results.get('totalResults')))
  print('Here are the metric totals for the matched total results.')
  totals = results.get('totalsForAllResults')

  for metric_name, metric_total in totals.iteritems():
    print('Metric Name  = %s' % metric_name)
    print('Metric Total = %s' % metric_total)
    print()


def print_rows(results):
  """Prints all the rows of data returned by the API.
  Args:
    results: The response returned from the Core Reporting API.
  """

  print('Rows:')
  if results.get('rows', []):
    for row in results.get('rows'):
      print('\t'.join(row))
  else:
    print('No Rows Found')

def print_realtime_report(results):
  print('**Real-Time Report Response**')
  print_report_info(results)
  print_profile_info(results.get('profileInfo'))
  print_column_headers(results.get('columnHeaders'))
  print_totals_for_all_results(results)


def main():
  # Define the auth scopes to request.
  scope = ['https://www.googleapis.com/auth/analytics.readonly']

  # Use the developer console and replace the values with your
  # service account email and relative location of your key file.
  # Account mail
  service_account_email = '****************@***********************'
  # P12 Certifcate
  key_file_location = 'C:\\****************.p12'

  # Authenticate and construct service.
  service = get_service('analytics', 'v3', scope, key_file_location,
    service_account_email)
  profile = get_first_profile_id(service)
  print_results(get_results(service, profile))


if __name__ == '__main__':
  main()