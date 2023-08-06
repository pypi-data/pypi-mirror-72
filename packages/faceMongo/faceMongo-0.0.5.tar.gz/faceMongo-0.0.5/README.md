***
## faceMongo
***
Scrape facebook public page and save it  in a mongo database as a collection of documents.
Retrieve a collection from mongo database.

***
### Installattion 
***

Run the following command in your terminal to install the package

```
pip install faceMongo
```
***
### Usage
***
**Scraping facebook public page**
Using `donaldtrump` and saviing it in a mongo database named `facebook`.  Assuming you have a mongo database
installed locally.

The following code will retrive and save the document in your mongo database

```
from faceMongo import faceMongo

fm = faceMongo.FaceMongo('facebook','localhost',27017) # database, host and port
fm.fb_page_to_db('donaldtrump') # scrape donaldtrump page to database

```

**Retrieving collection from the mongo database**
To retrive `donaldtrump` collection from the facebook database,
The code below will return the collection of documents in a list

```
docs = fm.docs_from_db('donaldtrump' )

```

***
### Licence
***
MIT License

