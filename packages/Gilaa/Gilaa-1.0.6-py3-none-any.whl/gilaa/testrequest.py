from urllib.parse import urlencode, quote_plus
import requests
import orbitize
authors_list = ["martínez", "watson", "möng"]
queries = []
encoded_queries = []
for i in authors_list:
    dict = {"author": i}
    queries.append(dict)
    encoded_queries.append(urlencode(dict,quote_via=quote_plus))

print(encoded_queries)

#query = {"author":"martínez neutron star"}
#encoded_query = urlencode(query,quote_via=quote_plus)
#print(encoded_query)

token="znay0PFTUbPmH2SXqMeRfg2hjRGDA5AnPz5Xn5jr"
r = []
# the query parameters can be included as part of the URL
for i in range(len(encoded_queries)):
    r.append(requests.get("https://api.adsabs.harvard.edu/v1/search/query?q=" + encoded_queries[i],\
                headers={'Authorization': 'Bearer ' + token}))
# the requests package returns an object; to get just the JSON API response, you have to specify this
    print(r[i].json())