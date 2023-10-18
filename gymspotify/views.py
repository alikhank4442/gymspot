from django.shortcuts import render
from .credentials import REDIRECT_URI, CLIENT_SECRET, CLIENT_ID
from rest_framework.views import APIView
from requests import Request, post
from rest_framework import status
from rest_framework.response import Response
from .util import update_or_create_user_tokens, is_spotify_authenticated
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from .util import *


class AuthURL(APIView):
    def get(self, request, format=None):
        scopes = 'user-read-playback-state user-modify-playback-state user-read-currently-playing'
        
        url = Request('GET', 'https://accounts.spotify.com/authorize', params = {
            'scope': scopes,
            'response_type': 'code',
            'redirect_uri': REDIRECT_URI, 
            'client_id': CLIENT_ID
        }).prepare().url
        
        return Response({'url': url}, status=status.HTTP_200_OK)

@api_view(('GET',))
def spotify_callback(request, format=None):
    code = request.GET.get('code')
    error = request.GET.get('error')
    print("***********check-1****************")
    print("code: ", code)
    print("**********************************")
    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'authorization_code', 
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }).json()
    print("*************check0*****************")
    print("resonsetype: ", type(response))
    print("response: ", response)
    print('******************************')
    
    access_token = response.get('access_token')
    token_type = response.get('token_type')
    refresh_token = response.get('refresh_token')
    expires_in = response.get('expires_in')
    print("************check************************")
    #print("expires_in: ", expires_in)
    #print("access_token: ", access_token)
    #print("refresh_token: ", refresh_token)
    expires_in = 3600
    print("************************************")
    error = response.get('error')
    
    #if not request.session.exists(request.session.session_key):
     #   request.session.create()
    
    #update_or_create_user_tokens(request.session.session_key, access_token, token_type, expires_in, refresh_token)       

    endpoint = "https://api.spotify.com/v1/recommendations?limit=10&market=PL&seed_artists=4NHQUGzhtTLFvgF5SZesLK&seed_genres=classical&seed_tracks=0c6xIDDpzE81m2q797ordA%2C2Q9nA56DKKJhj4cHMbHlAS"
    tokens = access_token
    headers = {'Content-Type': 'application/json', 'Authorization': "Bearer " + tokens} 
    try: 
        post(endpoint, headers=headers)
    except:
        put(endpoint,headers=headers)
    response = get(endpoint, {}, headers=headers)
    return Response({'Get Recomendation': response}, status=status.HTTP_200_OK)
    
    #return Response({'authorization token': access_token}, status=status.HTTP_200_OK)
    #return redirect
    
class IsAuthenticated(APIView):
    def get(self, request, format=None):
        is_authenticated = is_spotify_authenticated(self.request.session.session_key)
        return Response({'status': is_authenticated}, status =status.HTTP_200_OK)
    

class GetRecomendation(APIView):
    def get(self,request,format=None):
        #room_code = self.request.session.get('room_code')
        #room = Room.objects.filter(code=room_code)[0]
        host=self.request.session.session_key
        
        #endpoint = "https://api.spotify.com/v1/recommendations"
        endpoint = "https://api.spotify.com/v1/recommendations?limit=10&market=PL&seed_artists=4NHQUGzhtTLFvgF5SZesLK&seed_genres=classical&seed_tracks=0c6xIDDpzE81m2q797ordA%2C2Q9nA56DKKJhj4cHMbHlAS"
        response = execute_spotify_api_request(host, endpoint)
        print("--------------------------------------------------------------------------") 
        print("response: ", response)        
        print("--------------------------------------------------------------------------")
        
        return Response(response, status=status.HTTP_200_OK)
