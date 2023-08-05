# youtube-search-python


**A python script to return video links and titles by searching in YouTube. (Made from scratch without using YouTube API)**


A small python script that will return URLs and title names of videos when entering a keyword to search in youtube.
Feel free to use. 
Made from scratch.


Working as of June, 2020.


**Install**


```pip3 install youtube-search-python```


**Usage**


```python

from youtubesearchpython.searchyoutube import searchyoutube

##########Returns a array having two sub-arrays with video titles and links##########
result = searchyoutube("ENTER-YOUR-SEARCH-KEYWORD-HERE", "ENTER-SEARCH-OFFSET-HERE (default is 1)")

print(result[0]) #gives video links
print(result[1]) #gives video titles

##########Returns string "Network Error!" in case a network error is encountered##########

```


**Like the module?**


Consider starring the repo. Feel free to use.
