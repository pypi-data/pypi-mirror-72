# kaggleDownloader

Helps you download Kaggle Dataset to Google Colab Notebook or your own system in the current working directory (os.getcwd()) by using the Kaggle API Download Link and kaggle.json file obtained from the Kaggle account.


Specifications
======
Programming Language :- Python 3<br/>
Platforms Supported :- Google Colab Notebooks (Python 3) / Linux<br/>
Files Required :- kaggle.json (to be obtained from kaggle account; kaggle_profile -> My Account -> API -> Create new API token)<br/>

How to Use?
======
Add the kaggle.json file to your current working directory (os.getcwd(), the directory where you wish to download your dataset to)<br/>
By **three lines of code** you can download your kaggle dataset to your current working directory, either in Google Colab Notebooks or in your own system<br/>
The lines of code are as follows:-<br/>
&nbsp;&nbsp;&nbsp;&nbsp;1)if you are installing the package <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;a)on your own system<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**pip install kaggleDownloader** <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;b)on Google Colab Notebook<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**!pip install kaggleDownloader**<br/>
&nbsp;&nbsp;&nbsp;&nbsp;2)Import the get_dataset function from kaggleDownloader module<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**from kaggleDownloader import get_dataset**<br/>
&nbsp;&nbsp;&nbsp;&nbsp;3)call the get_dataset() function; there are two ways<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;a)**get_dataset()** or,<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;b)or you can pass the Kaggle Dataset Download API link in the get_dataset argument in string format (""); eg. SpringLeaf Dataset<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**get_dataset('kaggle competitions download -c springleaf-marketing-response')**<br/>

Follow along the instructions and you will be ready to work on your dataset.

