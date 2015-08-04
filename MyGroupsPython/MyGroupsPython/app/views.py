from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from app.authhelper import get_signin_url, get_token_from_code
import requests
import urllib

def home(request):
    # Redirect to groups
    return HttpResponseRedirect(reverse('groups'))

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# The following are routes specific to the web
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def groups(request):
    # If there is no token in the session, redirect to home
    access_token = request.session.get('access_token_web')
    if access_token == None:
        return HttpResponseRedirect(reverse('login'))
    else:
        # Send these headers with all API calls
        headers = { 'User-Agent' : 'python_tutorial/1.0',
                'Authorization' : 'Bearer {0}'.format(access_token),
                'Accept' : 'application/json' }
    
        # Perform the GET for groups using O365 Unified API
        response = requests.get("https://graph.microsoft.com/beta/me/joinedgroups", headers = headers, params = None)
        
        # Parse the API root for getting details (this includes the tenant)
        meta = response.json()['@odata.context']
        meta = meta[:meta.rfind('/')]
        
        # Render the view
        return render(  
            request,  
            'app/index.html',  
            context_instance = RequestContext(request,  
            {  
                'title':'My Groups',
                'request': request,  
                'groups': response.json()['value'],
                'apiroot': meta
            }))     

def detail(request, group_id): 
    # If there is no token in the session, redirect to home
    access_token = request.session.get('access_token_web')
    if access_token == None:
        return HttpResponseRedirect(reverse('login'))
    else:
        if request.GET.get('root', '') == '':
            return HttpResponseRedirect(reverse('groups'))
        else:
            # Send these headers with all API calls
            headers = { 'User-Agent' : 'python_tutorial/1.0',
                    'Authorization' : 'Bearer {0}'.format(access_token),
                    'Accept' : 'application/json' }
    
            # Perform the GET for groups using O365 Unified API
            url = request.GET.get('root', '') + '/groups/' + group_id + '/members'
            response = requests.get(url, headers = headers, params = None)
            
            # Render the view
            return render(  
                request,  
                'app/detail.html',  
                context_instance = RequestContext(request,  
                {  
                    'title':'My Group Memebership',
                    'request': request,  
                    'members': response.json()['value']
                }))     

def login(request):
    # Check for code returned from authorize
    auth_code = request.GET.get('code', '')
    if auth_code == '':
        redirect_uri = request.build_absolute_uri(reverse('login'))
        sign_in_url = get_signin_url(redirect_uri)
        
        # Render the view
        return render(  
            request,  
            'app/login.html',  
            context_instance = RequestContext(request,  
                {  
                    'title':'Login',
                    'request': request,  
                    'redirect': sign_in_url,
                    'isAddin': False
                }))  
    else:
          redirect_uri = request.build_absolute_uri(reverse('login'))
          access_token = get_token_from_code(auth_code, redirect_uri, "https://graph.microsoft.com")
          # Save the token in the session
          request.session['access_token_web'] = access_token
          return HttpResponseRedirect(reverse('groups'))


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# The following are routes specific add-ins
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!      
def addingroups(request): 
    # If there is no token in the session, redirect to home
    access_token = request.session.get('access_token_addin')
    if access_token == None:
        return HttpResponseRedirect(reverse('addinlogin'))
    else:
        # Send these headers with all API calls
        headers = { 'User-Agent' : 'python_tutorial/1.0',
                'Authorization' : 'Bearer {0}'.format(access_token),
                'Accept' : 'application/json' }
    
        # Perform the GET for groups using O365 Unified API
        response = requests.get("https://graph.microsoft.com/beta/me/joinedgroups", headers = headers, params = None)
        
        # Parse the API root for getting details (this includes the tenant)
        meta = response.json()['@odata.context']
        meta = meta[:meta.rfind('/')]
        
        # Render the view
        return render(  
            request,  
            'app/addin_index.html',  
            context_instance = RequestContext(request,  
            {  
                'title':'My Groups',
                'request': request,  
                'groups': response.json()['value'],
                'apiroot': meta
            }))

def addindetail(request, group_id): 
    # If there is no token in the session, redirect to home
    access_token = request.session.get('access_token_addin')
    if access_token == None:
        return HttpResponseRedirect(reverse('addinlogin'))
    else:
        if request.GET.get('root', '') == '':
            return HttpResponseRedirect(reverse('addingroups'))
        else:
            # Send these headers with all API calls
            headers = { 'User-Agent' : 'python_tutorial/1.0',
                    'Authorization' : 'Bearer {0}'.format(access_token),
                    'Accept' : 'application/json' }

            # First get the groups data again...could be cached instead
            groupsResponse = requests.get("https://graph.microsoft.com/beta/me/joinedgroups", headers = headers, params = None)
            
            # Parse the API root for getting details (this includes the tenant)
            meta = groupsResponse.json()['@odata.context']
            meta = meta[:meta.rfind('/')]

            # Perform the GET for groups using O365 Unified API
            url = request.GET.get('root', '') + '/groups/' + group_id + '/members'
            membershipResponse = requests.get(url, headers = headers, params = None)
            
            # Render the view
            return render(  
                request,  
                'app/addin_detail.html',  
                context_instance = RequestContext(request,  
                {  
                    'title':'My Group Memebership',
                    'request': request,  
                    'members': membershipResponse.content,
                    'groups': groupsResponse.json()['value'],
                    'apiroot': meta
                }))     

def addinlogin(request): 
    # Check for code returned from authorize
    auth_code = request.GET.get('code', '')
    if auth_code == '':
        redirect_uri = request.build_absolute_uri(reverse('addinlogin'))
        sign_in_url = get_signin_url(redirect_uri)
        
        # Render the view
        return render(  
            request,  
            'app/login.html',  
            context_instance = RequestContext(request,  
                {  
                    'title':'Login',
                    'request': request,  
                    'redirect': sign_in_url,
                    'isAddin': True
                }))  
    else:
          redirect_uri = request.build_absolute_uri(reverse('addinlogin'))
          access_token = get_token_from_code(auth_code, redirect_uri, "https://graph.microsoft.com")
          # Save the token in the session
          request.session['access_token_addin'] = access_token
          return HttpResponseRedirect(reverse('addingroups'))