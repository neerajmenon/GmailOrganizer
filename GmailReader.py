from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os.path

class GMailReader:
	def __init__(self):
		print('User Created')
		self.scopes = ['https://www.googleapis.com/auth/gmail.readonly']
		creds = None

		if os.path.exists('token-label.pickle'):
			with open('token-label.pickle', 'rb') as token:
				creds = pickle.load(token)

		try:
			if not creds or not creds.valid:
				if creds and creds.expired and creds.refresh_token:
					creds.refresh(Request())
				else:
					flow = InstalledAppFlow.from_client_secrets_file('credentials.json', self.scopes)
					creds = flow.run_local_server(port=0)
					with open('token-label.pickle', 'wb') as token:
						pickle.dump(creds, token)
		
				self.service = build('gmail', 'v1', credentials=creds)
		except Exception as error:
			print("Error occured while authenticating :-")
			print(error)
			
		print('GMail API auth completed')
 
	def get_messages(self, query, **kwargs): 
		try:
			obj = self.service.users().messages().list(userId='me', q=query, maxResults=kwargs.get('length', None)).execute()
			print('%s messages retrieved matching the given query.' % len(obj['messages']))
			return obj['messages']
		except Exception as error:
			print('Error occurred while searching :- %s' % error)
			return None