from __future__ import print_function
import argparse
import sys
from googleapiclient.errors import HttpError
from googleapiclient import sample_tools
from oauth2client.client import AccessTokenRefreshError


def main(argv):
  # Authenticate and construct service.
  service, flags = sample_tools.init(
      argv, 'analytics', 'v3', __doc__, __file__,
      scope='https://www.googleapis.com/auth/analytics.readonly')

  # Try to make a request to the API. Print the results or handle errors.
  try:
    first_profile_id = get_first_profile_id(service)
    if not first_profile_id:
      print('Could not find a valid profile for this user.')
    else:
      results = get_top_keywords(service, first_profile_id)
      print_results(results)

  except TypeError as error:
    # Handle errors in constructing a query.
    print(('There was an error in constructing your query : %s' % error))

  except HttpError as error:
    # Handle API errors.
    print(('Arg, there was an API error : %s : %s' %
           (error.resp.status, error._get_reason())))

  except AccessTokenRefreshError:
    # Handle Auth errors.
    print ('The credentials have been revoked or expired, please re-run '
           'the application to re-authorize')


def get_first_profile_id(service):

  accounts = service.management().accounts().list().execute()

  if accounts.get('items'):
    firstAccountId = accounts.get('items')[0].get('id')
    webproperties = service.management().webproperties().list(
        accountId=firstAccountId).execute()

    if webproperties.get('items'):
      firstWebpropertyId = webproperties.get('items')[0].get('id')
      profiles = service.management().profiles().list(
          accountId=firstAccountId,
          webPropertyId=firstWebpropertyId).execute()

      if profiles.get('items'):
        return profiles.get('items')[0].get('id')

  return None


def get_top_keywords(service, profile_id):
  return service.data().ga().get(
      ids='ga:' + profile_id,
      start_date='2012-01-01',
      end_date='2012-01-15',
      metrics='ga:visits',
      dimensions='ga:source,ga:keyword',
      sort='-ga:visits',
      filters='ga:medium==organic',
      start_index='1',
      max_results='25').execute()


def print_results(results):

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


if __name__ == '__main__':
  main(sys.argv)
  
  
  Regras básicas da Daily Scrum

Para que a Scrum Meeting possa funcionar de forma efetiva, existem algumas regras que devem ser estabelecidas e mantidas pelo Scrum Master:

Duração máxima de 15 minutos (No nosso caso será 25 minutos. Se ficar ruim alteramos novamente)
- Assim como os demais eventos do Scrum, essas reuniões possuem um tempo fixo.
- Reuniões longas e monótonas são ótimas formas de começar mal o dia (acaba com a energia das pessoas).
- As reuniões não podem ultrapassar 15 minutos, pois após esse tempo, as pessoas começam a se distrair e perder o foco principal, deixando a reunião pouco produtiva.

Mesmo local e horários todos os dias
- O objetivo dessa regra é fazer com que as pessoas se acostumem e passem a sentir que essas reuniões fazem parte de sua rotina diária.
- A reunião deve iniciar mesmo quando algum membro da equipe ainda não tenha chegado, ou caso alguém tenha que faltar.

Todos os membros do time devem responder três perguntas
1.	O que eu fiz desde a última Daily Scrum?
2.	O que vou fazer hoje?
3.	Quais são os impedimentos que estão me atrapalhando de realizar meu trabalho?

Com as respostas para essas perguntas, a equipe organiza meios de resolver os impedimentos, contando com a ajuda do Scrum Master, que tem como uma de suas funções remover os impedimentos que surgem durante o andamento do projeto e atrapalham o Time de Desenvolvimento.

Vale ressaltar que a resolução dos problemas levantados durante a reunião não é feita durante a reunião, mas após o evento com as pessoas envolvidas. 
