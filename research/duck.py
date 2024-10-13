from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper

search = DuckDuckGoSearchRun()
search2 = DuckDuckGoSearchResults()
search3 = DuckDuckGoSearchResults(backend="news")
wrapper = DuckDuckGoSearchAPIWrapper(time="d", max_results=2)
search4 = DuckDuckGoSearchResults(api_wrapper=wrapper, source="news")

while True:
    req = input("Aske a duck")
    if req == "quit":
        quit()
    res = search.run(req)
    print()
    print(res)
    print("{{{{{{{")
    res = search2(req)
    print()
    print(res)
    print("99999999")
    res = search3(req)
    print()
    print(res)
    print("99999999")
    res = search4(req)
    print()
    print(res)
    print("Wrapper")
