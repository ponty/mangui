from easyprocess import EasyProcess, EasyProcessError
from entrypoint2 import entrypoint
from path import path
import tempfile

manlifter_output = 'foobar.man.xml'


class ManLifterError(Exception):
    pass


def docxml(command):
    tmpdir = path(tempfile.mkdtemp(prefix='manlifter_'))
    path('/usr/bin/manlifter').symlink(tmpdir / 'manlifter')

    p = EasyProcess([tmpdir / 'manlifter', command], cwd=tmpdir)
    p.check()

    try:
        xml = path(tmpdir / manlifter_output).text()
    except IOError:
        s = EasyProcessError(p)
        raise ManLifterError(s)
    tmpdir.rmtree()

    return xml


@entrypoint
def test(command='grep'):
    print(docxml(command))


