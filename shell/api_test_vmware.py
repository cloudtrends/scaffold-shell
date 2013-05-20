#! /usr/bin/env python
# By: Kelcey Damage, 2012

import hashlib, hmac, base64, urllib, urllib2, json
import sys


# Reference GET/POST Sample request
#
#1. http://10.10.0.1:8080/client/api
#2. ?apiKey=c32UUyjuyrMmTUO_mmqqvOGIWHaWmcdG0bs4CV7aAC15v9dIG7fdVoHp6gNZ3WtlzMb2kvNrTLA5QA8ab_DEUQ
#3. &command=listVirtualMachines
#4. &response=json
#5. &zoneid=1
#6. &signature=QlOwk0DfY6j9KWqWsNGuvjxD7tY%3D

# Reference sample input:
#


#




apikey="pWvfiUpCUxi0H_iGpsUSEKLHhv0Y0a3BBfi2R_oI_ho4TF254NzxAGCZP85N7H0CtXKHRaypoE-h9jvYRoOuwg"
secret="B2NfXq__OliEUlEpGqjefja8tCMt3rxD-WaiygdAatI2KhIp9oGIgypm3GHxypoufRJjycRnvJduvOkgUUwx8A"






apikey="5JiTB6qmNq5ebfEZfCOudpvy4OR6lUck3GkSCEhQbstihzW4gGyWgnDZ-EA1KPS8-5XP4pkMiv6y82rfiBDL6Q"
secret="skzM50sU9_qQHclpNqLKugEfPRrYv-6BW6eR8inAl8No_zFNgA29pmYWl_fJ7JNTWFTFozMBwRKJO0J4GeKDbw"

if len( sys.argv ) < 2 :
	print " please give me ip and action type "
	exit() 


host_ip= sys.argv[ 1]

command_type=sys.argv[2]

if "deployMonitorVm" == command_type :
	network_id = sys.argv[ 3 ]
	master_ip = sys.argv[ 4 ]
	print "user input network id is :",network_id
	request={ 'command':'deployMonitorVm', 'id':'200','template_name':'monitor-101' , 'response':'json' , 'networkId':'200' }
	request[ 'command' ] = 'deployMonitorVm'
	request[ 'template_name' ] = 'monitor-appliance-vmware'
	#request[ 'template_name' ] = 'monitor-101'
	request[ 'response' ] = 'json'
	request[ 'networkId' ] = network_id
	request[ 'id' ] =  network_id
	request[ 'master_ip' ] =  master_ip
	request[ 'zoneid' ] =  "1"
	request[ 'podid' ] =  "1"
	request[ 'clusterid' ] =  "1"
if "stopMonitorVm" == command_type:
	print "begin stop monitor vm"
	mvm_id = sys.argv[3]
	request['command'] = "stopMonitorVm"
	request['id'] = str( mvm_id )
	request['response']= "json"
if "destroyMonitorVm" == command_type:
	print "begin stop monitor vm"
	mvm_id = sys.argv[3]
	request['command'] = "destroyMonitorVm"
	request['id'] = str( mvm_id )
	request['response']= "json"
if "stopMonitorVm" == command_type:
	print "begin stop monitor vm"
if "stopMonitorVm" == command_type:
	print "begin stop monitor vm"





api_url = "http://"+ host_ip +":8080/client/api"


class SignedAPICall(object):
	def __init__(self, api_url, apikey, secret):
		self.api_url = api_url
		self.apikey = apikey
		self.secret = secret

	def request(self, args):
		args['apiKey'] = self.apikey

		self.params = []
		print "request args:",args
		self._sort_request(args)
		self._create_signature()
		self._build_url_request()
		self._response()

	def _sort_request(self, args):
		keys = sorted(args.keys())

		for k in keys:
			self.params.append(k + '=' + urllib.quote_plus(args[k]))

	def _create_signature(self):
		self.query = '&'.join(self.params)
		digest = hmac.new(
			self.secret, 
			msg=self.query.lower(), 
			digestmod=hashlib.sha1).digest()

		self.signature = base64.b64encode(digest)

	def _build_url_request(self):
		self.query += '&signature=' + urllib.quote_plus(self.signature)
		self.value = self.api_url + '?' + self.query
		
	def _response(self):
		print "current url is :",self.value
		response = urllib2.urlopen(self.value)
		self.decoded = json.loads(response.read())
		self.decoded= json.dumps(self.decoded, sort_keys=True, indent=4) 

# Example Usage:
#
# api.value is a debug that holds the complete valid URL request.
#
# api.decoded is the response from executing the API request.

api = SignedAPICall(api_url, apikey, secret)
api.request(request)
print api.value
print api.decoded
