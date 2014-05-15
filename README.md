amazonses-dsl
=============

A simple DSL for Amazon SES API to send emails

Create your AmazonSes Object whit:
>amazonses_api.AmazonSes(access_key,secret_key)

And send emails with: (it returns a message_id)
>amazonobject.send_mail(emailfrom,subject,htmlbody,[listemail_TO])
