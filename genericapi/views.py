from rest_framework import status,views
from rest_framework.response import Response

class VersionAPIView(views.APIView):
    
    def get(self,request):
        api_details = {
            'Generic API':'1.0.0',
            'Info' : {
                'Version' : '1.0.0',
                'Title' : 'Generic API',
                'Author' : 'Mr. Aniket Chandrakant Dhole',
                'Description' : 'This api contains starting apps or modules of backend.This apps is common or generally use for any website ',
            },
            'License' : {
                'MIT' : '2021',
            },
            'Contact' : {
                'Email' : 'aniketdhole123456789@gmail.com',
                'Phone' : '+919284770231',
            },
            'About' : {
                'Profile' : 'https://aniketdhole.netlify.app',
                'Github' : 'https://github.com/aniket1004',
            }
        }
        return Response(api_details,status = status.HTTP_200_OK)