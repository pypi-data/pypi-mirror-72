# gab_toolbox
Package containing functions frequently used by me in other scripts
## How to install:
You can fork the rep or use pip:
 ``` python
 pip install gab_toolbox
 ```
## List of tools:

Here I will list and briefly describe the classes and functions contained.

## format_tools
Functions used for importing and writing files, formatting dictionaries and lists. To import use:  
 ``` python
 from gab_toolbox import format_tools
 ```
To use the specific function:
 ``` python
 format_tools.arr2dic(arguments)
 ```
 
### valid_title:

Function used to check and eventually modify strings used for saving file names in case they contain not accepted symbols. 
```python
valid_title(title,[char])
```
The function checks if the string or array of strings specified in **title** is valid and returns the string/s with the invalid character/s replaced with a valid character set **= '_'** by [default]. If you want to change the substituting character  just change the **[char]** entry.

### import_file:
Function used to import files as an array. Every new line is a new entry of the array.

```python
importtxt(file)
```
In **file** you must specify the name and extension of the file you want to import and, if the file is not located in the working directory, you must add the full file path.

### write_file:
Function used to write text files from arrays. Every array entry will be written in a separeted line.

```python
write(array,file)
```

+ In **array** you must write the target array that needs to be exported. 
+ In **file** you must specify the name and extension. The full path name must be specified if you don't want the file in the working directory. 

### dic2arr:

Function used to convert dictionaries to a 2D array. Every entry corrisponds to a dict entry.

```python
dic2arr(dictionary,[order],[sort],[rev])
```
+ The first argument accepts the **dictionary** variable and it's the only obligatory argument. 
+ The **[order]** argument controls how the array is filled; for **order=0** [default] the resulting array will follow the dict order [key, value], for **order=1** the opposite.
+ The **[sort] and [rev]** arguments control the order of the array; for **sort = 1** the array will be sorted following an ascending order of the first value and then the second value of each array, for **rev = 1** the sorting order will be discending. By default **sort=0 and rev=0**.

### arr2dic
Function used to convert 2D arrays in dictionaries. The array needs to be formatted as **[[*key*,*value*],...]** and every array will corrispond to a dict entry.

```python
arr2dic(array,[sort],[rev],[overwrite])
```
+ The first argument accepts the **array** variable and it's the only obligatory argument. 
+ The **[sort] and [rev]** argument control the order of the dictionary; for **sort = 1** the dictionary will be sorted following an ascending order of the first value of each array, for rev = 1 the sorting order will be discending. By [default] **sort=0 and rev=0**.
+ The **[overwrite]** argument gives the possibility to merge multiple *values* under the same *key*; for **overwrite=0** [default] the values will be merged while for **overwrite=1** it will only save the last *value* corresponding to the *key*.


## tex_tools

Functions that can be used for latex.

### bib_entries:
This function is used to separate and classify bib files, imported as list.
```python
bib_entries(bib_array,crit)
```

+ **bib_array** accepts the imported bib file as a list.
+ **crit** is the criterion you want to extrapolate form the bib entries. They are:
    + by_ref: extrapolate the ref name,
    + by_date: extrapolate the publication date,
    + by_title: extrapolate the title,
    + by_author: extrapolate the author

The list can be manually expanded and modified if the user needs different criterions or uses a different format. The format is the following:
```python
'by_date': ['\tyear','{','}','by date'],
```
The first argument finds the symbol or string that identifies the line that contains the key. The second and third arguments are used to find and isolate the value of the key. For e.g. the **date** key is located in the line that starts with **\tyear** and the value is delimited by { }: 
>\tyear={2005}.

The fourth argument is a descriptor and it is optional.
The function returns a 2D array with the choosen criterion as string and the corresponding entry as list.

### order_bib:
```python
order_bib(bib_array,[order],[form],[crit])
```
Function used to sort the array. 
+ The first argument accept any array that is formatted as the ouput of bib_entries ([key,[entry]]) or the imported bib file as list. if you want to use directly the order bib you must set the **[form]** argument to 1 and specify the criterion.
+ The **[order]** argument is used to define the type of sorting: ascending (0) or descending (1).

The function returns as the first argument the sorted bib entries ready to be saved and the corresponding sorted array with [key,[entry]] format.



### filter_bib:
```python
order_bib(bib_array,key_word,[form],[crit])
```
Function used to filter the array based on the key argument. 
+ The first argument accepts any array that is formatted as the ouput of bib_entries ([key,[entry]]) or the imported bib file as list. if you want to use directly the order bib you must set the **[form]** argument to 1 and specify the criterion.
+ The second argument is used to filter the entries. It compares the user input to the key argument of the bib_array.

The function returns all the corresponding entries ordered by appearance as bib entries ready to be saved and the corresponding sorted array with [key,[entry]] format.



### ttt
```python
ttt(file_array,[sep])
```
This function converts any imported csv files as list to a list ready to be saved that follows latex table format.
+ The first argument accepts the original csv file (imported as list) to be converted.
+ The **[sep]** argument defines the column separator. By default is set to \t (tab).

