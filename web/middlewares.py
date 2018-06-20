"""
This class holds middlewares related to the frontend
"""


class PreviousUrl:
    def __init__(self, get_response):
        """
         Middleware constructor
         :param get_response: gets the last middleware response
        """
        self.get_response = get_response
        self.urls = []


    def __call__(self, request):
        """
        Process and return the previous url
        :param request:
        :return: previous_url
        """
        self.urls.append(request.path_info)
        unique_urls = []
        excluded_urls = ['/robots.txt']

        for url in self.urls:
            if url in excluded_urls:
                continue
            elif url in unique_urls:
                unique_urls.remove(url)
                unique_urls.append(url)
            else:
                unique_urls.append(url)

        request.previous_url = unique_urls[-2] if len(unique_urls) > 1 else unique_urls[-1]
        response = self.get_response(request)
        return response

