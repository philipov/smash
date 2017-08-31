

'''
basic assumptions about the properties of dependencies
'''

#----------------------------------------------------------------------#

def test__OrderedSet():
    from ordered_set import OrderedSet

    s = OrderedSet()
    s.add(3)
    s.add(2)
    s.add(3)
    s.add(1)
    s.add(2)

    assert s == (3,2,1)


#----------------------------------------------------------------------#
