'''Get whois results'''
import scraptools
import re
import pprint


def get_whois_html(url):
    base_url = 'http://www.whois.com/whois/'
    query = url.replace('http://www.', '').replace('https://www.', '')
    search_url = base_url + query
    html = scraptools.getUrlContent(search_url)
    return html


def get_whois_result(html):
    result = '\n'.join(re.findall('whois_result.*?>(.*?)</div>', html))
    result = result.replace('<br>', '\n').replace('&nbsp;', ' ')
    # results = re.sub('Name servers:(.+\w{4}.+?(\s+)[0-9.]+)+', ': ', results, flags=re.DOTALL)
    return result


def result_to_dict(result):
    ret = {}
    subd = None
    for line in result.splitlines():
        comps = line.split(': ')
        if len(comps) == 1 and len(comps[0]) and comps[0][-1] == ':':
            subd = dict()
            ret[comps[0].strip(':')] = subd

        if len(comps) == 2:
            k, v = map(str.strip, comps)
            if len(k) == len(comps[0]):
                ret[k] = v
            else:
                subd[k] = v

    return ret


def test_whois(use_cache):
    if use_cache:
        html = open('result.txt').read()
    else:
        html = get_whois_html('polymtl.ca')
        with open('result.txt', 'w') as f:
            f.write(html)

    result = get_whois_result(html)
    infos = result_to_dict(result)
    pprint.pprint(infos)


def main():
    html = get_whois_html('polymtl.ca')
    result = get_whois_result(html)
    infos = result_to_dict(result)
    pprint.pprint(infos)


if __name__ == '__main__':
    main()