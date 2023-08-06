# GitLas :Git Log Statistics 
The minimalist Git Log Statistics library

## Meta Data of Git
Often times we have a ton of Meta Data ,but we really don't have much of tools to make useful
analysis from it.
Git Logs are one of the best sources from which we can actually understand and analyse some of the trends in our Project workings.

The commits and merges can be tracked easily with git , but to make useful charts and analysis we need to convert these data into a useful data type.

GitLas is a simple Library that filters out gitlogs with regular expression pattern matching and applies useful analytic filters to get more out of the data. JSON data type is highly preferred and widely used, hence the library convert the git log into a simple JSON format which can be exported as well. 

These statistics can be useful or not really useful at all depending on the size of your project and the collaborators associated with it.
## Getting GitLog as text
To get the git log in a text format
   
```
$ git log > gitlog.txt
```

or copy it to the clipboard and later paste it in a new file.  

```
$ git log > clip
```
## Requirements
### Python 3  
## Installing gitlas 
using pip

```
$ pip install gitlas
``` 
or pip3 in some systems  

```
$ pip3 install gitlas
```
