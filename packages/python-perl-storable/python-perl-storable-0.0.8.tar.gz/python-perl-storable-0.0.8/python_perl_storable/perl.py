import subprocess

def freeze_perl(value, init=''):
    """ Заморозка на perl. 
        value - строка. Код на perl
    """
    p = subprocess.Popen(["perl", "-e", "%suse Storable; $Storable::canonical=1; print Storable::freeze(%s)" 
        % (init, value)], stdout=subprocess.PIPE)
        
    output, err = p.communicate()

    if p.returncode != 0:
        raise IOError("returncode=%s" % p.returncode)
    return output


def thaw_perl(value, init='', noout=0):
    """ Разморозка на perl. 
        value - строка. Код на python
    """
    value = '"%s"' % (('%s' % value)[2:-1])

    x = subprocess.call(["perl", "-e", "%suse Storable; use Data::Dumper; %s(Storable::thaw(%s))" 
        % (init, ("" if noout else "print STDERR Dumper"), value)])

    if x != 0:
        raise IOError("returncode=%s" % x)