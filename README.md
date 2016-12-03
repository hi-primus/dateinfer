pydateinfer
===========

Python library to infer date format from examples.  This is an actively
 maintained fork of the original [dateinfer](https://github.com/jeffreystarr/dateinfer)
 library by Jeffery Starr.  It maintains python 2/3 compatibility and 
 will be released as pydateinfer.  Pull requests and issues welcome.

Table of Contents
-----------------

* [Problem Statement](#problem-statement)
* [Installation](#installation)
* [Usage](#usage)

<a name="problem-statement"></a>Problem Statement
-------------------------------------------------

Imagine that you are given a large collection of documents and, as part of the extraction process, extract date
 information and store it in a normalized format. If the documents follow a single schema, the ideal approach
 is to craft a date parsing string for the schema. However, if the documents follow different schemas or if the
 contents are noisy (e.g. date fields were hand-populated), the development can become onerous.

This library makes a "best guess" on the proper date parsing string (`datetime.strptime`) based on examples in
the file.

<a name="installation"></a>Installation
---------------------------------------

The simplest way to install the library will be once we get the first 
release cut:

````
$ pip install pydateinfer
````

<a name="usage"></a>Usage
-------------------------

````Python
>>> import dateinfer
>>> dateinfer.infer(['Mon Jan 13 09:52:52 MST 2014', 'Tue Jan 21 15:30:00 EST 2014'])
'%a %b %d %H:%M:%S %Z %Y'
>>>
````

Give `dateinfer.infer` a list of example date strings. `infer` returns a `datetime.strftime`/`strptime`-compliant
date format string for its "best guess" of a format string that will correctly parse the majority of the examples.


