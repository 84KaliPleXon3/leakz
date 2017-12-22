#!/usr/bin/env python
# -*- coding:utf-8 -*-

import re
import sys
import string


def save_document(filename, document):
    with open(filename, 'wb') as f:
        f.write(document.encode('utf-8'))


def load_document(filename):
    try:
        with open(filename, 'rb') as f:
            return f.readlines()
    except IOError as e:
        print e
        sys.exit(1)


def remove_escaped(text):
    r = re.compile(r'\&\#(\d+);')

    for m in r.findall(text):
        c = int(m)

        try:
            text = text.replace('&#{};'.format(c), unichr(c))
            print u'[I] Replaced {} with {}'.format('&#{};'.format(c), unichr(c)).encode('utf-8')
        except ValueError as e:
            pass

    pattern = {'&Yuml;': u'\u0178', '&permil;': u'\u2030', '&rlm;': u'\u200f',
               '&tilde;': u'\u02dc', '&emsp;': u'\u2003', '&Dagger;': u'\u2021',
               '&quot;': '"', '&OElig;': u'\u0152', '&lt;': '<', '&lsquo;': u'\u2018',
               '&scaron;': u'\u0161', '&lrm;': u'\u200e', '&ldquo;': u'\u201c',
               '&zwj;': u'\u200d', '&rsaquo;': u'\u203a', '&sbquo;': u'\u201a',
               '&ensp;': u'\u2002', '&thinsp;': u'\u2009', '&lsaquo;': u'\u2039',
               '&rsquo;': u'\u2019', '&amp;': '&', '&Scaron;': u'\u0160', '&gt;': '>',
               '&ndash;': u'\u2013', '&euro;': u'\u20ac', '&rdquo;': u'\u201d',
               '&oelig;': u'\u0153', '&dagger;': u'\u2020', '&mdash;': u'\u2014',
               '&zwnj;': u'\u200c', '&bdquo;': u'\u201e', '&circ;': u'\u02c6'}

    for k, v in pattern.iteritems():
        text = text.replace(k, v)
        print u'[I] Replaced {} with {}'.format(k, v)

    return text


def match_ip_address(document):
    return re.match(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', document)


def match_mail_address(document):
    return re.search(r'\b[\w.+-]+?@[\w]+[.]+[-_.\w]+\b', document)


def filter_printable(document):
    return filter(string.printable.__contains__, document)


def main():
    if len(sys.argv) < 3:
        sys.exit(1)

    document_lines = load_document(sys.argv[1])
    password_list = []

    for document in document_lines:
        document = document.decode('utf-8').strip('\n').strip('\r')
        document = remove_escaped(document)
        document = filter_printable(document)

        if not match_ip_address(document) and not match_mail_address(document):
            password_list.append(document)

    save_document(sys.argv[2], '\n'.join(password_list))


if __name__ == '__main__':
    main()
