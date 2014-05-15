import amazonses_api

access_key = 'ACCESS_KEY'
secret_key = 'ACCESS_PASSWORD_KEY'

sender = 'send@example.com'
subject = 'Subject Cool'
htmlbody = '<html><head><h1>Title</h1></head><body>Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.<button>Call to action</button></body></html>'

amazonobject = amazonses_api.AmazonSes(access_key,secret_key)

filedb = open( "db.txt", "r" )
linesd = filedb.readlines()
for i, line in enumerate(linesd):
	message_id = amazonobject.send_mail(sender,subject,htmlbody,[linesd[i]],email_format='html')
filedb.close()