from mangui.manlift import docxml
from mangui.parser import command_info

commands = '''
ls
grep
echo
cat
pwd
date
clear
sudo
clear
'''.strip().splitlines()


def test_manlift():
    for x in commands:
        print x
        assert docxml(x)


def test_command_info():
    for x in commands:
        print x
        assert command_info(x)
