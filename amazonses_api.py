import hmac
import hashlib
import base64
import urllib
import urllib2

from datetime import datetime
from xml.dom import minidom

class AmazonSes(object):

  def __init__(self, access_key, secret_id):
    self._access_key = access_key
    self._secret_id = secret_id
    self.base_url = 'https://email.us-east-1.amazonaws.com'


  def _sign(self, message):
    """Sign an AWS request"""
    signed_hash = hmac.new(key=self._secret_id, msg=message, digestmod=hashlib.sha256)
    return base64.b64encode(signed_hash.digest()).decode()


  def _call(self, command, params=None):
    """Make a call to SES"""
    params = params or {}
    params['Action'] = command
    now = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
    headers = {
      'Content-Type':'application/x-www-form-urlencoded',
      'Date':now,
      'X-Amzn-Authorization':'AWS3-HTTPS AWSAccessKeyId=%s, Algorithm=HMACSHA256, Signature=%s' %
                             (self._access_key, self._sign(now))
    }
    data = urllib.urlencode(params)
    data = data.encode('utf-8')
    req = urllib2.Request(self.base_url, data, headers)
    try: 
    	resp = urllib2.urlopen(req)
    except urllib2.HTTPError as e:
    	print e.code
    	print e.read
    else:
      xml = minidom.parseString(resp.read())
      return xml.getElementsByTagName('MessageId')[0].firstChild.nodeValue

  def send_mail(self, source, subject, body, to_addresses,
                cc_addresses=None, bcc_addresses=None, email_format='text',
                callback=None, reply_addresses=None, return_path=None):
    """Composes an email and sends it"""
    known_formats = {
      'html':'Message.Body.Html.Data',
      'text':'Message.Body.Text.Data'
    }
    singular = {
      'Source': source,
      'Message.Subject.Data':subject
    }
    if email_format not in known_formats:
      raise ValueError("Format must be either 'text' or 'html'")
    singular[known_formats[email_format]] = body
    if return_path:
      singular['ReturnPath'] = return_path
    multiple = AwsMultipleParameterContainer()
    multiple['Destination.ToAddresses.member'] = to_addresses
    if cc_addresses:
      multiple['Destination.CcAddresses.member'] = cc_addresses
    if bcc_addresses:
      multiple['Destination.BccAddresses.member'] = bcc_addresses
    if reply_addresses:
      multiple['ReplyToAddresses.member'] = reply_addresses
    params = dict(singular, **multiple)
    message_id = self._call('SendEmail', params)
    return message_id



class AwsMultipleParameterContainer(dict):
  """Build a parameters list as required by Amazon"""

  def __setitem__(self, key, value):
    if isinstance(value, basestring):
      value = [value]
    for i in range(1, len(value) + 1):
      dict.__setitem__(self, '%s.%d' % (key, i), value[i - 1])