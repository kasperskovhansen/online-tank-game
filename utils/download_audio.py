import urllib.request

class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.69 Safari/537.36"

def download_audio(username):
    urllib._urlopener = AppURLopener()
    url = 'https://translate.google.com.vn/translate_tts?ie=UTF-8&q=' + str(username) + '&tl=da&client=tw-ob'
    urllib._urlopener.retrieve(url, 'sounds/usernames/' + str(username) + '.mp3')