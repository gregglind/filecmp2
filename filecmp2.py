'''
Bettercomp

A filecmp replacement for python

'''

from filecmp import *

try:
    import json
except ImportError:
    import simplejson as json



def _signature(stuffaboutfile):
    ''' what is the signature to use for 'shallow' comparison'''
    pass

def default_same(f1,f2):
    ''' read and compare'''
    pass

extension_dict = defaultdict(default_same)
extension_dict['xml'] = ians_same_xml
extension_dict['json'] = json.load
extension_dict['ini'] = some_file_from_configparser

'''others might be:

dot
??
??
'''


def dirs_same_enough(dir1,dir2,report=False,filetypes_to_check_for_exact=[]):
    ''' use os.walk and filecmp.cmpfiles to
    determine if two dirs are 'same enough'.
    
    Args:
        dir1, dir2:  two directory paths
        report:  if True, print the filecmp.dircmp(dir1,dir2).report_full_closure()
              before returning / exiting
        filetypes_to_check_for_exact: if defined, a list of suffixes, like 'dot'
            that will be checked.
    
    Returns:
        bool, or report_full_closure()
    
    >>> import os
    >>> d1 = io.TempIO()
    >>> d1.a = 'somedir'
    >>> _ = d1.a.putfile('blah','txt1')
    >>> d2 = io.TempIO()
    >>> d2.a = 'somedir'
    >>> _ = d2.a.putfile('blah','txt2')
    >>> dirs_same_enough(d1,d2)
    False
    >>> d3 = io.TempIO()
    >>> d3.a = 'somedir'
    >>> _ = d3.a.putfile('blah','txt1')
    >>> dirs_same_enough(d1,d3)
    True
    '''
    # os walk:  root, list(dirs), list(files)
    # those lists won't have consistent ordering,
    # os.walk also has no guaranteed ordering, so have to sort.
    walk1 = sorted(list(os.walk(dir1)))
    walk2 = sorted(list(os.walk(dir2)))
    
    def report_and_exit(report,bool_):
        if report:
            filecmp.dircmp(dir1,dir2).report_full_closure()
            return bool_
        else:
            return bool_
    
    if len(walk1) != len(walk2):
        return false_or_report(report)

    for (p1,d1,fl1),(p2,d2,fl2) in zip(walk1,walk2):
        d1,fl1, d2, fl2 = set(d1),set(fl1),set(d2),set(fl2)
        if d1 != d2 or fl1 != fl2:
            return report_and_exit(report,False)
        
        files = fl1
        if filetypes_to_check_for_exact:
            files = [x for x in fl1 if x.split('.')[-1] in filetypes_to_check_for_exact]
        
        if True:
            same,diff,weird = filecmp.cmpfiles(p1,p2,files,shallow=False)
            if diff or weird:
                return report_and_exit(report,False)
    
    return report_and_exit(report,True)




from lxml.etree import fromstring as totree


################################
## from ianb's formencode...
def text_compare(t1, t2):
    if not t1 and not t2:
        return True
    if t1 == '*' or t2 == '*':
        return True
    return (t1 or '').strip() == (t2 or '').strip()

def xml_compare(x1, x2, reporter=None):
    if x1.tag != x2.tag:
        if reporter:
            reporter('Tags do not match: %s and %s' % (x1.tag, x2.tag))
        return False
    for name, value in x1.attrib.items():
        if x2.attrib.get(name) != value:
            if reporter:
                reporter('Attributes do not match: %s=%r, %s=%r'
                         % (name, value, name, x2.attrib.get(name)))
            return False
    for name in x2.attrib.keys():
        if name not in x1.attrib:
            if reporter:
                reporter('x2 has an attribute x1 is missing: %s'
                         % name)
            return False
    if not text_compare(x1.text, x2.text):
        if reporter:
            reporter('text: %r != %r' % (x1.text, x2.text))
        return False
    if not text_compare(x1.tail, x2.tail):
        if reporter:
            reporter('tail: %r != %r' % (x1.tail, x2.tail))
        return False
    cl1 = x1.getchildren()
    cl2 = x2.getchildren()
    if len(cl1) != len(cl2):
        if reporter:
            reporter('children length differs, %i != %i'
                     % (len(cl1), len(cl2)))
        return False
    i = 0
    for c1, c2 in zip(cl1, cl2):
        i += 1
        if not xml_compare(c1, c2, reporter=reporter):
            if reporter:
                reporter('children %i do not match: %s'
                         % (i, c1.tag))
            return False
    return True


