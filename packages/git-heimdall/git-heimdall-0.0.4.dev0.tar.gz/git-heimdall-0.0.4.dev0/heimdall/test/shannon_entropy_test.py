import unittest
import heimdall.codescan.plugins.entropy as entropy

class ShannonEntropy(unittest.TestCase):

    def test_shannon_entropy(self):
        files = '/Users/s0s0249/workspace/open_source/git-heimdall/heimdall/test/sample_secrets1.txt'
        f = open(files, 'r')
        text = f.readlines()
        shannon_entropy = entropy.ShannonEntropy()
        for s in text:
            score = shannon_entropy.scan(s)
            print ('Str: ',s, ' Entropy: ',score)
        f.close()    
if __name__ == '__main__':
    unittest.main()
