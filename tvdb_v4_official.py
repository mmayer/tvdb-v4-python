import json
import urllib
import urllib.request
from urllib.error import HTTPError


class Auth:
    def __init__(self, url, apikey, pin=""):
        loginInfo = {"apikey": apikey}
        if pin != "":
            loginInfo["pin"] = pin

        loginInfoBytes = json.dumps(loginInfo, indent=2).encode('utf-8')
        req = urllib.request.Request(url, data=loginInfoBytes)
        req.add_header("Content-Type", "application/json")
        with urllib.request.urlopen(req, data=loginInfoBytes) as response:
            res = json.load(response)
            self.token = res["data"]["token"]

    def get_token(self):
        return self.token


class Request:
    def __init__(self, auth_token):
        self.auth_token = auth_token
        self.links = None

    def make_request(self, url):
        req = urllib.request.Request(url)
        req.add_header("Authorization", "Bearer {}".format(self.auth_token))
        try:
            with urllib.request.urlopen(req) as response:
                res = json.load(response)
        except HTTPError as e:
            try:
                res = json.load(e)
            except:
                res = { }
        data = res.get("data", None)
        if data is not None and res.get('status', 'failure') != 'failure':
            self.links = res.get("links", None)
            return data
        msg = res.get('message', None)
        if not msg:
            msg = 'UNKNOWN FAILURE'
        raise ValueError("failed to get " + url + "\n  " + str(msg))


class Url:
    def __init__(self):
        self.base_url = "https://api4.thetvdb.com/v4/"

    def construct(self, url_sect, url_id=None, url_subsect=None, url_lang=None, **query):
        url = self.base_url + url_sect
        if url_id:
            url += '/' + str(url_id)
        if url_subsect:
            url += '/' + url_subsect
        if url_lang:
            url += '/' + url_lang
        if query:
            query = { var: val for var, val in query.items() if val is not None }
            if query:
                url += '?' + urllib.parse.urlencode(query)
        return url


class TVDB:
    def __init__(self, apikey: str, pin=""):
        self.url = Url()
        login_url = self.url.construct('login')
        self.auth = Auth(login_url, apikey, pin)
        auth_token = self.auth.get_token()
        self.request = Request(auth_token)

    def get_req_links(self) -> dict:
        return self.request.links

    def get_artwork_statuses(self, meta=None) -> list:
        """Returns a list of artwork statuses"""
        url = self.url.construct('artwork/statuses', meta=meta)
        return self.request.make_request(url)

    def get_artwork_types(self, meta=None) -> list:
        """Returns a list of artwork types"""
        url = self.url.construct('artwork/types', meta=meta)
        return self.request.make_request(url)

    def get_artwork(self, id: int, meta=None) -> dict:
        """Returns an artwork dictionary"""
        url = self.url.construct('artwork', id, meta=meta)
        return self.request.make_request(url)

    def get_artwork_extended(self, id: int, meta=None) -> dict:
        """Returns an artwork extended dictionary"""
        url = self.url.construct('artwork', id, 'extended', meta=meta)
        return self.request.make_request(url)

    def get_all_awards(self, meta=None) -> list:
        """Returns a list of awards"""
        url = self.url.construct('awards', meta=meta)
        return self.request.make_request(url)

    def get_award(self, id: int, meta=None) -> dict:
        """Returns an award dictionary"""
        url = self.url.construct('awards', id, meta=meta)
        return self.request.make_request(url)

    def get_award_extended(self, id: int, meta=None) -> dict:
        """Returns an award extended dictionary"""
        url = self.url.construct('awards', id, 'extended', meta=meta)
        return self.request.make_request(url)

    def get_all_award_categories(self, meta=None) -> list:
        """Returns a list of award categories"""
        url = self.url.construct('awards/categories', meta=meta)
        return self.request.make_request(url)

    def get_award_category(self, id: int, meta=None) -> dict:
        """Returns an award category dictionary"""
        url = self.url.construct('awards/categories', id, meta=meta)
        return self.request.make_request(url)

    def get_award_category_extended(self, id: int, meta=None) -> dict:
        """Returns an award category extended dictionary"""
        url = self.url.construct('awards/categories', id, 'extended', meta=meta)
        return self.request.make_request(url)

    def get_content_ratings(self, meta=None) -> list:
        """Returns a list of content ratings"""
        url = self.url.construct('content/ratings', meta=meta)
        return self.request.make_request(url)

    def get_countries(self, meta=None) -> list:
        """Returns a list of countries"""
        url = self.url.construct('countries', meta=meta)
        return self.request.make_request(url)

    def get_all_companies(self, page=None, meta=None) -> list:
        """Returns a list of companies"""
        url = self.url.construct('companies', page=page, meta=meta)
        return self.request.make_request(url)

    def get_company_types(self, meta=None) -> list:
        """Returns a list of company types"""
        url = self.url.construct('companies/types', meta=meta)
        return self.request.make_request(url)

    def get_company(self, id: int, meta=None) -> dict:
        """Returns a company dictionary"""
        url = self.url.construct('companies', id, meta=meta)
        return self.request.make_request(url)

    def get_all_series(self, page=None, meta=None) -> list:
        """Returns a list of series"""
        url = self.url.construct('series', page=page, meta=meta)
        return self.request.make_request(url)

    def get_series(self, id: int, meta=None) -> dict:
        """Returns a series dictionary"""
        url = self.url.construct('series', id, meta=meta)
        return self.request.make_request(url)

    def get_series_extended(self, id: int, meta=None) -> dict:
        """Returns a series extended dictionary"""
        url = self.url.construct('series', id, 'extended', meta=meta)
        return self.request.make_request(url)

    def get_series_episodes(self, id: int, season_type: str="default", page: int=0, lang: str=None, meta=None) -> dict:
        """Returns a series episodes dictionary"""
        url = self.url.construct('series', id, 'episodes/'+season_type, lang, page=page, meta=meta)
        return self.request.make_request(url)

    def get_series_translation(self, id: int, lang: str, meta=None) -> dict:
        """Returns a series translation dictionary"""
        url = self.url.construct('series', id, 'translations', lang, meta=meta)
        return self.request.make_request(url)

    def get_all_movies(self, page=None, meta=None) -> list:
        """Returns a list of movies"""
        url = self.url.construct('movies', page=page, meta=meta)
        return self.request.make_request(url)

    def get_movie(self, id: int, meta=None) -> dict:
        """Returns a movie dictionary"""
        url = self.url.construct('movies', id, meta=meta)
        return self.request.make_request(url)

    def get_movie_extended(self, id: int, meta=None) -> dict:
        """Returns a movie extended dictionary"""
        url = self.url.construct('movies', id, 'extended', meta=meta)
        return self.request.make_request(url)

    def get_movie_translation(self, id: int, lang: str, meta=None) -> dict:
        """Returns a movie translation dictionary"""
        url = self.url.construct('movies', id, 'translations', lang, meta=meta)
        return self.request.make_request(url)

    def get_all_seasons(self, page=None, meta=None) -> list:
        """Returns a list of seasons"""
        url = self.url.construct('seasons', page=page, meta=meta)
        return self.request.make_request(url)

    def get_season(self, id: int, meta=None) -> dict:
        """Returns a season dictionary"""
        url = self.url.construct('seasons', id, meta=meta)
        return self.request.make_request(url)

    def get_season_extended(self, id: int, meta=None) -> dict:
        """Returns a season extended dictionary"""
        url = self.url.construct('seasons', id, 'extended', meta=meta)
        return self.request.make_request(url)

    def get_season_types(self, meta=None) -> list:
        """Returns a list of season types"""
        url = self.url.construct('seasons/types', meta=meta)
        return self.request.make_request(url)

    def get_season_translation(self, id: int, lang: str, meta=None) -> dict:
        """Returns a seasons translation dictionary"""
        url = self.url.construct('seasons', id, 'translations', lang, meta=meta)
        return self.request.make_request(url)

    def get_episode(self, id: int, meta=None) -> dict:
        """Returns an episode dictionary"""
        url = self.url.construct('episodes', id, meta=meta)
        return self.request.make_request(url)

    def get_episode_extended(self, id: int, meta=None) -> dict:
        """Returns an episode extended dictionary"""
        url = self.url.construct('episodes', id, 'extended', meta=meta)
        return self.request.make_request(url)

    def get_episode_translation(self, id: int, lang: str, meta=None) -> dict:
        """Returns an episode translation dictionary"""
        url = self.url.construct('episodes', id, 'translations', lang, meta=meta)
        return self.request.make_request(url)

    get_episodes_translation = get_episode_translation # Support the old name of the function.

    def get_all_genders(self, meta=None) -> list:
        """Returns a list of genders"""
        url = self.url.construct('genders', meta=meta)
        return self.request.make_request(url)

    def get_all_genres(self, meta=None) -> list:
        """Returns a list of genres"""
        url = self.url.construct('genres', meta=meta)
        return self.request.make_request(url)

    def get_genre(self, id: int, meta=None) -> dict:
        """Returns a genres dictionary"""
        url = self.url.construct('genres', id, meta=meta)
        return self.request.make_request(url)

    def get_all_languages(self, meta=None) -> list:
        """Returns a list of languages"""
        url = self.url.construct('languages', meta=meta)
        return self.request.make_request(url)

    def get_person(self, id: int, meta=None) -> dict:
        """Returns a people dictionary"""
        url = self.url.construct('people', id, meta=meta)
        return self.request.make_request(url)

    def get_person_extended(self, id: int, meta=None) -> dict:
        """Returns a people extended dictionary"""
        url = self.url.construct('people', id, 'extended', meta=meta)
        return self.request.make_request(url)

    def get_person_translation(self, id: int, lang: str, meta=None) -> dict:
        """Returns an people translation dictionary"""
        url = self.url.construct('people', id, 'translations', lang, meta=meta)
        return self.request.make_request(url)

    def get_character(self, id: int, meta=None) -> dict:
        """Returns a character dictionary"""
        url = self.url.construct('characters', id, meta=meta)
        return self.request.make_request(url)

    def get_people_types(self, meta=None) -> list:
        """Returns a list of people types"""
        url = self.url.construct('people/types', meta=meta)
        return self.request.make_request(url)

    get_all_people_types = get_people_types # Support the old function name

    def get_source_types(self, meta=None) -> list:
        """Returns a list of source types"""
        url = self.url.construct('sources/types', meta=meta)
        return self.request.make_request(url)

    get_all_sourcetypes = get_source_types # Support the old function name

    # kwargs accepts args such as: page=2, action='update', type='artwork'
    def get_updates(self, since: int, **kwargs) -> list:
        """Returns a list of updates"""
        url = self.url.construct('updates', since=since, **kwargs)
        return self.request.make_request(url)

    def get_all_tag_options(self, page=None, meta=None) -> list:
        """Returns a list of tag options"""
        url = self.url.construct('tags/options', page=page, meta=meta)
        return self.request.make_request(url)

    def get_tag_option(self, id: int, meta=None) -> dict:
        """Returns a tag option dictionary"""
        url = self.url.construct('tags/options', id, meta=meta)
        return self.request.make_request(url)

    def get_all_lists(self, page=None, meta=None) -> dict:
        url = self.url.construct('lists', page=page, meta=meta)
        return self.request.make_request(url)

    def get_list(self, id: int, meta=None) -> dict:
        url = self.url.construct('lists', id, meta=meta)
        return self.request.make_request(url)

    def get_list_extended(self, id: int, meta=None) -> dict:
        url = self.url.construct('lists', id, 'extended', meta=meta)
        return self.request.make_request(url)

    def get_list_translation(self, id: int, lang: str, meta=None) -> dict:
        """Returns an list translation dictionary"""
        url = self.url.construct('lists', id, 'translations', lang, meta=meta)
        return self.request.make_request(url)

    def get_inspiration_types(self, meta=None) -> dict:
        url = self.url.construct('inspiration/types', meta=meta)
        return self.request.make_request(url)

    def search(self, query, **kwargs) -> list:
        """Returns a list of search results"""
        url = self.url.construct('search', query=query, **kwargs)
        return self.request.make_request(url)

    def get_tags(self, slug: str) -> dict:
        """Returns a tag option dictionary"""
        url = self.url.construct('entities', url_subsect=slug)
        return self.request.make_request(url)
