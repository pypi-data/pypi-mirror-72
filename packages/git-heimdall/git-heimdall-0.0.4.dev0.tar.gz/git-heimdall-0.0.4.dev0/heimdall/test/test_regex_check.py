import unittest
import heimdall.codescan.plugins.check_regex as regex

class RegexTest(unittest.TestCase):

    def test_regex(self):
        print("Run test")
        str = ['wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY',
               'helloThisIsAVeryBigStatement',
               'helloThisIsAVeryBigStatementButThisShouldNotBeDetectedInTheEntropyCheck.ThisIs100Sure',
               '73756e6e79736861726d61',
               '73756e6e79736861726d61AddingSomeTextLetsSeeWhatHappens',
               'aslkfslfkslk/LDKFLKFLKDFLK/sldfksjlkfslfkSomethingThatDoesn\'tMakeSense.salfksalfk',
               'password',
               '-----BEGIN RSA PRIVATE KEY-----salfkjlsakfjlskfjsalfkjalfkjaslfkslfk-----END RSA PRIVATE KEY-----',
               'password : password',
               'passphrase : passphrase',
               'password : pass@123',
               'pw : password@123',
               'passphrase : password@123',
               'pass : password@123',
               'extractPasswordFromConfigFile(password=None)',
               'for eg: `Pass : foo@123`'
        ]
        _regex = regex.RegexCheck()
        for s in str:
            print(_regex.scan(s))

if __name__ == '__main__':
    unittest.main()
