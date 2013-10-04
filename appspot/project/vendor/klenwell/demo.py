"""
    Klenwell Demo Module

    A simple module created specifically to test vendor imports in the
    Appswell framework.

    Usage:
    from project.vendor.klenwell.demo import VendorDemo
    VendorTest = VendorDemo()
    assert(VendorTest.is_loaded == True)
    assert(VendorTest.test() == 'success')
"""

class VendorDemo(object):
    """
    A simple class for testing and demonstration purposes
    """
    is_loaded = True

    def test(self):
        return 'success'
