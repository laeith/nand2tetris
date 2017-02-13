import os
import HackAssembler
import unittest


class TestHackAssembler(unittest.TestCase):
    """ Provides a quick utility for checking if HackAssembler correctly compiles Hack Language into
     Hack machine code. The main test (test_all_files) goes through all *.asm files inside ../tests
     directory and compares the output for each file with its reference file (*.hack),
     reference files were created using the assembler provided by Nand2Tetris staff.
    """
    def test_all_files(self):
        files = os.listdir("../tests/")
        outcomes = []
        for file in files:
            if file.endswith(".asm"):
                compare_file = open("../tests/" + file[:-4] + ".hack", 'r')

                translation = HackAssembler.assemble("../tests/" + file)
                expected_translation = [line.strip() for line in compare_file]

                result = True
                for line1, line2 in zip(translation, expected_translation):
                    if line1[2] != line2:
                        result = False
                outcomes.append((file, result))

                compare_file.close()

        for outcome in outcomes:
            self.assertEqual(outcome[1], True, "%s has FAILED" % outcome[0])
            if outcome[1]:
                print("%s has been successfully compiled to machine code." % (outcome[0]))
            else:
                print("%s has FAILED during compilation to machine code." % (outcome[0]))

    @staticmethod
    def single_test(file_name):
        """ Method intended for manual debugging / usage. """
        translation = HackAssembler.assemble(file_name + ".asm")
        with open("../tests/" + file_name + ".hack", 'r') as source:
            expected = []
            for line in source:
                expected.append(line.strip())
        result = True
        for line1, line2 in zip(translation, expected):
            if line1[2] != line2:
                print("Line %s: %s -> %s (%s) -> %s (%s)" % (line1[0], line1[1], line1[2],
                                                             int(line1[2], 2), line2,
                                                             int(line2, 2)))
                result = False
        print(result)


if __name__ == '__main__':
    unittest.main()
