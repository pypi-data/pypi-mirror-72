import unittest
import pprint
from heimdall.codescan.plugins import manager

class CodescanPluginManagerTest(unittest.TestCase):

    def test_plugin_manager(self):
        print("Run test")
        files = ['/Users/s0s0249/workspace/open_source/git-heimdall/heimdall/test/sample_secrets.txt']
        _codescan_plugin_manager = manager.CodescanPluginManager()
        val = _codescan_plugin_manager.scan('/Users/s0s0249/workspace/open_source/git-heimdall/heimdall/test/', ['sample_secrets.txt', 'sample_secrets1.txt'])
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(val)

if __name__ == '__main__':
    unittest.main()
