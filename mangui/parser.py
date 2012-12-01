from entrypoint2 import entrypoint
from manlift import docxml
import pprint
import re
import xml.etree.ElementTree as ET


def tidy_elem(xml):
    toremove = re.compile('<.+?>').findall(xml)
    for x in toremove:
        xml = xml.replace(x, ' ')
    xml = xml.replace('\r', '')
    xml = xml.replace('\n', '')

    return xml.strip()

esc_ls = '''
&acute;
&nbsp;
&bsol;
&ldquo;
&rdquo;
&shy;
'''.strip().splitlines()


def tidy(xml):
    xml = xml.replace('&copy', 'copy')
    for x in esc_ls:
        xml = xml.replace(x, ' ')
    return xml.strip()


def parse(xml):
    xml = tidy(xml)

    all_options = []
    tree = ET.fromstring(str(xml))
    variablelists = tree.findall('.//variablelist')
    for x in variablelists:
        for varlistentry in x.findall('varlistentry'):
            options = varlistentry.find('term').findall('option')
            listitem = varlistentry.find('listitem')
            descr = tidy_elem(ET.tostring(listitem))
            if len(options):
                all_options.append(([x.text for x in options], descr))

    ls = tree.findall('.//refpurpose')
    refpurpose = tidy_elem(ET.tostring(ls[0]))

    def fkey(x):
        x = x[0][0]
        x = x.replace('-', '')
        x = x.lower()
        return x

    all_options.sort(key=fkey)
    return dict(
            options=all_options,
            purpose=refpurpose,
            )


def command_info(cmd):
    d = parse(docxml(cmd))
    d['command'] = cmd
    return d


@entrypoint
def test():
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(command_info('grep'))


