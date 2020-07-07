## Introduction
This repository provides a fast and convenient way to extract structured information from internet. It is mainly based on
the wonderful [CC](https://commoncrawl.org) (CommonCrawl) project and the other two packages from 
[lxuc](https://github.com/lxucs) (i.e.[the client](https://github.com/lxucs/cdx-index-client) that retrieves related 
urls from the CDX Index API and [the project](https://github.com/lxucs/commoncrawl-warc-retrieval) that downloads 
related warc files) which facilitate the extraction of target html pages.

However, even though the downloading process of target html pages is no more a problem, thanks to many projects like
those two mentioned above, the parsing of the html pages is still somehow a challenge, especially when it comes to 
extract structured information from raw html pages. For instance, the repository **commoncrawl-warc-retrieval** shows 
how to parse html pages by two examples, i.e. parser-cnn.py and parser-nytimes.py. This means that you have to write 
your own codes for individual projects. 

In this repository, we modify the codes from **commoncrawl-warc-retrieval and additionally utilize the awesome package 
[Goose](https://github.com/goose3/goose3) to simplify the parsing process. With the help of Goose, we are able to
extract several important fields from raw html pages with ease. In **parse.py**, we try to parse the raw warc file and 
its html content in a more general way so that we don't need to examine the structure of web pages on a case-by-case 
basis. Another improvement is that we add some lines of codes so that the encoding of html pages can be recognized and
avoid wrong encodings during the parsing process.

Moreover, this repository utilizes the power of multiprocessing and visualizes the progress by the package 
[p_tqdm](https://github.com/swansonk14/p_tqdm).

## How to install
Step 1. git clone this repository
$ git clone https://github.com/zrxbeijing/CommonCrawl-Parser

Step 2. install packages in the requirements.txt
$ pip install -r requirements.txt

Step 3. git clone the following two projects

$ cd CommonCrawl-Parser
$ git clone https://github.com/lxucs/cdx-index-client
$ git clone https://github.com/lxucs/commoncrawl-warc-retrieval


## How to use
Step 1. retrieve corresponding index files which contains related html pages. For example, suppose we want to extract 
info related to www.SomeDomain.com/SubCategory/* scraped by CC (CommonCrawl),

$ python cdx-index-client/cdx-index-client.py www.SomeDomain.com/SubCategory/* -d output_idx -j

Step 2. download related warc files from Amazon S3.

$  python commoncrawl-warc-retrieval/cdx-index-retrieval.py output_idx output_warc

Note: for a detailed tutorial regarding how to search for related index and related warc files, see 
this [blog](https://liyanxu.blog/2019/01/19/retrieve-archived-pages-using-commoncrawl-index/)

Step 3. parse the warc file into structured data

$ python parse.py output_warc

In the end, an excel file "result.xlsx" is generated.

## Extract other fields in the html page
If more fields needs to be extracted from the raw html pages, we could make use of the awesome package 
[BeautifuSoup](https://pypi.org/project/bs4/). To that end, We just need to modify the parse_html method in **parse.py**.
