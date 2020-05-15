import google_images_download
import requests


class Data:
    def find(self, name):
        '''Gets string and returns the string page code on Wikipedia.
        If there is no such page, returns None.
        If there is a page with a similar name, returns False.
        '''
        try:
            r = requests.get(
                eval(
                    requests.get(
                        f'https://he.wikipedia.org/w/api.php',
                        params={
                            'action': 'opensearch',
                            'search': name,
                            'limit': 1,
                            'namespace': 0,
                            'format': 'json'}).text)[3][0]).text
        except:
            return None
        if "האם התכוונתם ל..." in r:
            return False
        return r

    def Images(self, limit, name):
        # Gets limit(integer) and string and returns list of limit images.
        self.response = google_images_download.googleimagesdownload()
        arguments = {"keywords": name, "limit": limit, "silent_mode": True}
        self.paths = self.response.download(arguments)
        return self.paths[0].get(name)


if __name__ == '__main__':
    data = Data()
    print(data.find('איליי הוא הומו'))
    print(data.Images(5, 'אייל גולן'))
