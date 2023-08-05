
FileIOPy
===================


This is the simple File IO package for python. It can save your time.



Install
-------------

    pip install FileIOPy

## Features

 - Easy to use 
 - Time saver
 - Many intresting functions 

## Documents

You have setup like this - 

```python
from FileIOPy import FileIOPy
file = FileIOPy.FileIOPy('file.txt')
```
These are the functions list -    
> - **write_file :** Using this Function, You can write any content in your file  
you can write your content in two types:  
: write mode  
 if you choose write mode, first your file data will clear and then you can write your content
: Continue mode  
 if you choose continue mode, you can write your content without losing any data
 
> - **read_file :** Using this function, you read your file data

> - **read_lines :** Read files line by line

> - **clear_file :** Clears the all data of the file

> - **check_length :** Check how many alphabates in your file have

> - **search_file:** Returns True if entered content exists in your file

> - **count_file:** returns how many times your content exists in your file
> 
And many more...

You can use like these - 

    a = file.read_file()
    print(a)
   Result
   

    Hello world!
