
import datetime

TITLE 			= 'My Anime'
ART_DEFAULT 	= 'art-default.jpg'
ICON_DEFAULT 	= 'icon-default.png'
ICON_PREFS		= 'Gear.png'
ICON_SEARCH		= 'Search.png'

####################################################################################################


####################################################################################################

def ValidatePrefs():
	pass

def Start():
	HTTP.CacheTime = 0
	HTTP.Headers['Cache-Control'] = 'no-cache'
	ObjectContainer.title1 = TITLE
	ObjectContainer.art = R(ART_DEFAULT)
	DirectoryObject.thumb = R(ICON_DEFAULT)
	DirectoryObject.art = R(ART_DEFAULT)
	VideoClipObject.thumb = R(ICON_DEFAULT)
	VideoClipObject.art = R(ART_DEFAULT)

def GetUserId():
	user=Prefs['user']
	if not user:
		return "1"
	if (user=='Default'):
		return "1"
	if (user=='Family Friendly'):
		return "2"
	if (user=='User 3'):
		return "3"
	if (user=='User 4'):
		return "4"
	if (user=='User 5'):
		return "5"
	if (user=='User 6'):
		return "6"
	if (user=='User 7'):
		return "1"
	if (user=='User 8'):
		return "1"
	if (user=='User 9'):
		return "1"
	if (user=='User 10'):
		return "1"
	return "0"

def GetServerUrl():
	ip="localhost"
	port="8111"
	if Prefs['ip']:
		ip=Prefs['ip']
	if Prefs['port']:
		port=Prefs['port']
	Log("Preferences "+ip+":"+port)
	return "http://"+ip+":"+port+"/"

@route('/video/jmm/empty')
def Empty():
	return ""
def GetLimit():
	limit="20"
	if Prefs['limit']:
		limit=Prefs['limit']
	return limit

#if JMMServer is at localhost, and Plex Home Theater or other client is outside, and need directplay, this will ensure it gets the right ip for streaming
def RedirectUrlIfNeeeded(url):
	host = Request.Headers.get('Host', '127.0.0.1:32400')
	host="http://"+host.split(':')[0:][0]+":"
	if ("http://192.168." in host) or ("http://10." in host) or ("http://172.16." in host) or ("http://172.17." in host) or ("http://172.18." in host) or ("http://172.19." in host) or ("http://172.20." in host) or ("http://172.21." in host) or ("http://172.22." in host) or ("http://172.23." in host)  or ("http://172.24." in host) or ("http://172.25." in host) or ("http://172.26." in host) or ("http://172.27." in host) or ("http://172.28." in host)  or ("http://172.29." in host) or ("http://172.30." in host) or ("http://172.31." in host):
		url=url.replace("http://127.0.0.1:",host)
		url=url.replace("http://localhost:",host)
	return url

@handler('/video/jmm', TITLE, art=ART_DEFAULT, thumb=ICON_DEFAULT)
def MainMenu():
	try:
		req = HTTP.Request(url=GetServerUrl()+"JMMServerPlex/GetFilters/"+GetUserId(),timeout=10)
		if req.content:
			Response.Headers['Content-type']="text/xml;charset=utf-8"
			return req.content.replace('</MediaContainer>','<Directory prompt="Search" thumb="'+R(ICON_SEARCH)+'" art="'+R(ICON_SEARCH)+'" key="/video/jmm/search" title="Search" search="1"/><Directory title="Preferences" thumb="'+R(ICON_PREFS)+'" art="'+R(ICON_PREFS)+'" key="/:/plugins/com.plexapp.plugins.myanime/prefs" settings="1"/></MediaContainer>')
		else:
			Log("My Anime Url: "+GetServerUrl()+"JMMServerPlex/GetFilters/"+GetUserId()+" returns empty, check if the user has categories assigned");
			oc = ObjectContainer(title2='My Anime')
			oc.add(DirectoryObject(key = Callback(Empty), title='Invalid User, please verify preferences'))
			oc.add(PrefsObject(title = 'Preferences', thumb = R(ICON_PREFS), art= R(ICON_PREFS)))
		return oc
	except Exception, e:
		Log("My Anime Exception: "+str(e))
		oc = ObjectContainer(title2='My Anime')
		oc.add(DirectoryObject(key = Callback(Empty), title='Error connecting to JMM Server, please verify preferences ('+str(e)+')'))
		oc.add(PrefsObject(title = 'Preferences', thumb = R(ICON_PREFS), art= R(ICON_PREFS)))
		return oc

@route('/video/jmm/search')
def Search(query):
	req = HTTP.Request(url=GetServerUrl()+"JMMServerPlex/Search/"+GetUserId()+"/"+GetLimit()+"/"+String.Quote(query),timeout=240)
	Response.Headers['Content-type']="text/xml;charset=utf-8"
	return req.content

@route('/video/jmm/proxy/{url}')
def Proxy(url,includeExtras='0',includeRelated='0',includeRelatedCount='0'):
	url = url.decode("hex")
	Response.Headers['Content-type']="text/xml;charset=utf-8"
	url = RedirectUrlIfNeeeded(url);
	req = HTTP.Request(url=url,timeout=240)
	return req.content



####################################################################################################