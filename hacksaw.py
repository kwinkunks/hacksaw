import re
import urllib2
import json


# These are regexs
aliases = {
    'GR': ['gamma', 'gapi'],
    'DT': ['slowness', 'acoustic.+?travel', 'usec\/ft'],
    'RT': ['resistivity',],
}

def fuzzy_lookup(mnemonic):
    """
    Gets a result from fuzzyLAS.
    """
    url = "http://fuzzylas.org/lookup?mnemonic={0}&method=simple&guesses=1&format=json".format(mnemonic)
    r = urllib2.urlopen(url)
    
    return json.loads(r.readlines()[0])
  


def get_alias(fuzzylas_json=None):
    """
    Takes a result from fuzzyLAS and finds an alias.
    """
    if not fuzzylas_json:
        print "ERROR: No JSON"
        return None
        
    for k, v in fuzzylas_json[0].items():
        for result in v:
            for a, l in aliases.items():
                # a is the key to alias to
                # l is the list of words to recognize
                f = re.IGNORECASE
                regex = re.compile(r'(\b' + r'\b|\b'.join(l) + r'\b)', flags=f)
                if regex.search(result['description']) or regex.search(result['unittype']):
                    return a
                    
def get_aliases(curves):
    result = {}
    for nasty in curves:
        nice = get_alias(fuzzy_lookup(nasty))
        if nice:
            result[nice] = nasty
    return result
                    