from goose3 import Goose
import os
import logging
from p_tqdm import p_map
import pandas as pd
import argparse
from bs4 import BeautifulSoup


def parse_warc(warcfile):
    """
    Read warc files and parse it into several important information.
    :param warcfile: the file path of a warcfile.
    :return: html.
    """
    # figure out encoding of the file
    with open(warcfile, 'rb') as warc:
        lines = warc.readlines()
        html_idx = None
        for index, line in enumerate(lines):
            if line.startswith(b'<!DOCTYPE'):
                html_idx = index
                break
        if html_idx is None:
            logging.info('Abort %s: no html pages found' % warcfile)
            return None
        # separate the scraper header and the html page
        header = lines[:html_idx]
        raw_html = lines[html_idx:]

        # check the response status code
        response_idx = None
        for index, line in enumerate(header):
            if line.startswith(b'HTTP'):
                response_idx = index
                break

        if response_idx is None:
            logging.info('Abort %s: no status code found' % warcfile)
            return None

        response_line = header[response_idx]
        if b'200' not in response_line:
            logging.info('Abort %s: response status code not 200' % warcfile)
            return None

        charset_idx = None
        for index, line in enumerate(header):
            if b'charset=' in line:
                charset_idx = index
                break

        if charset_idx is None:
            encoding = 'UTF-8'
        else:
            encoding = header[charset_idx].split(b'charset=')[-1].strip().decode(encoding='UTF-8')

        html = "\n".join([line.decode(encoding=encoding) for line in raw_html])
        return html


def parse_html(html):
    """
    Parse html. Leverage goose and bs4 to parse html efficiently.
    :param html: html string.
    :return: a dict containing news information.
    """
    g = Goose()
    article = g.extract(raw_html=html)
    url = article.final_url
    title = article.title
    text = article.cleaned_text

    # extra coding blocks for other fields
    # soup = BeautifulSoup(html)
    # related_field = soup.find(path)

    return {'url': url,
            'title': title,
            'text': text}


def extract_info(warcfile):
    """
    A wrapper function to be passed into the multiprocessing pool.
    :param warcfile: file path of a warcfile.
    :return: result containing news information.
    """
    html = parse_warc(warcfile)
    if html:
        return parse_html(html)
    else:
        return None

def do_work(file_paths):
    """
    Enable multiprocessing. Inherently implement multiprocessing.
    :param num_process:
    :return:
    """
    result = p_map(extract_info, file_paths)
    return result


def result_to_excel(result):
    """
    Export result to excel.
    :param result: a result list containing dics which are records of news.
    :return: None. Output an excel file.
    """
    dic = {'url': [],
           'title': [],
           'text': []}
    for row in result:
        if row:
            dic['url'].append(row['url'])
            dic['title'].append(row['title'])
            dic['text'].append(row['text'])
        else:
            dic['url'].append(None)
            dic['title'].append(None)
            dic['text'].append(None)

    df = pd.DataFrame(dic)
    df.to_excel('result.xlsx')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='parse html pages')
    parser.add_argument('warc_path', metavar='W', type=str, default=None, help='Where you store the warc files')
    args = parser.parse_args()
    files = os.listdir(args.warc_path)
    file_paths = [os.join(args.warc_path, file) for file in files]
    result = do_work(file_paths)
    result_to_excel(result)

