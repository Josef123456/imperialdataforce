#  Copyright (c) 2017 Michal Kazmierski 
#  
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#  
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#  
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.


"""Simple Python wrapper for Deezer's REST API"""

import requests

DEEZER_ROOT_URL = 'https://api.deezer.com'

class DeezerAPI:

    """The main access point for Deezer API.
       Methods:
        get(self, endpoint, id_)
        search(self, query, strict=None, order=None)
    """ 
    valid_endpoints = ['album',
                       'artist', 
                       'chart', 
                       'comment', 
                       'editorial', 
                       'episode', 
                       'genre', 
                       'infos', 
                       'options', 
                       'playlist', 
                       'podcast', 
                       'radio', 
                       'track', 
                       'user']

    def __init__(self):
        self.session = requests.Session()
       
    def _make_get_request(self, url,  params=None):

        """Make the actual GET request to Deezer API"""
    
        limit = {'limit': 1000000}
        try:
            params.update(limit)
        except AttributeError:
            params = limit

        res = self.session.get(url, params=params).json()
        if 'error' in res.keys():
            raise DeezerAPIError(res.get('error'))

        return res
    
    def get(self, endpoint, id_, field=None):

        """Get the data for object with particular id from an endpoint.
           Params:
            endpoint: string
                the API endpoint to query
            id_: string
                the id of the requested object
            field: string, optional, default None
                the field to get for endpoints that support it
            Return: res, dict
                the result of API call

            Examples:
                

            Read more: http://developers.deezer.com/api
        """

        if endpoint not in self.valid_endpoints:
            raise ValueError('{} is not a valid Deezer API endpoint. Valid options are: {}'.format(endpoint, ', '.join(self.valid_endpoints)))

        if not field:
            field = ''

        request_url = '/'.join((DEEZER_ROOT_URL, endpoint, id_, field))
        res = self._make_get_request(request_url)

        return res

    def search(self, query, strict=None, order=None):

        """Search for tracks matching query.
           Params:
            query: string
                the query to run
            strict: string, optional, default None:
                enable strict mode (no fuzzy matching), set to 'on'
            order: string, optional, default None:
                return results in a particular order. Available options are
                RANKING, TRACK_ASC, TRACK_DESC, ARTIST_ASC, ARTIST_DESC, 
                ALBUM_ASC, ALBUM_DESC, RATING_ASC, RATING_DESC, DURATION_ASC, DURATION_DESC

          Return: res, dict
            the result of API call

          Read more: http://developers.deezer.com/api/search
        """

        params = {'q': query, 'strict': strict, 'order': order}
        url = DEEZER_ROOT_URL + '/search'
        res = self._make_get_request(url, params=params)
        return res


class DeezerAPIError(Exception):
    
    def __init__(self, result):
        self.result = result
        self.err_msg = self.result.get('message', 'unknown error')
        self.err_code = self.result.get('code', '-1')

        super().__init__(self)

    def __str__(self):
        return '{} - {}'.format(self.err_code, self.err_msg)

