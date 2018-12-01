from winesSearcher import Searcher

searcher = Searcher()
print("searcher is initialized")

region = input('Enter the region: ')
wine = searcher.searchRandomByRegion(region)
print(wine)

typ = input('Enter the typ: ')
wine = searcher.searchRandomByType(typ)
print(wine)
