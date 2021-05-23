from rest_framework import renderers
import json 

class UserRender (renderers.JSONRenderer):
    charset = 'utf-8'
    def render(self,data,accepted_media_type=None,renderer_context=None):
        response = ''
        print(str(data))
        if 'ErrorDetail' in str(data):
            response = json.dumps({'errors':data})
        else:
            response = json.dumps({'success':data})
        return response