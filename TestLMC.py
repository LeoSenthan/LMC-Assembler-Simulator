from LMC import LMC
import unittest
from unittest.mock import patch
import io

class TestLMC(LMC):
    def load_program(self):
        try:
            with open(self.filename, "r") as f:
                data = f.read().strip()
        except FileNotFoundError:
            raise FileNotFoundError(f"Machine code file '{self.filename}' was not found.")

        instructions = [int(data[i:i + 3]) for i in range(0, len(data), 3)]
        if len(instructions) > 100:
            raise ValueError(f"Program exceeds 100 memory locations ({len(instructions)}).")
        for i, instr in enumerate(instructions):
            self.memory[i] = instr

class TestPrintOutput(unittest.TestCase):
    def test(self):
        unittest_paths = ["ADD.lmc","BRA.lmc","BRP.lmc","BRZ.lmc","LDA.lmc","STA.lmc","SUB.lmc"]
        correct_outputs = ["ACC: 15","ACC: 20","ACC: 50","ACC: 1","ACC: 10","ACC: 30","ACC: 5"]
        path = "unittests/correct_machine_code/"

        for ix in range(len(unittest_paths)):    
            lmc = TestLMC(path + unittest_paths[ix])
            with patch('sys.stdout', new=io.StringIO()) as test:
                lmc.run()
                self.assertEqual(test.getvalue().strip(), correct_outputs[ix])
            print("SUCCESSFUL FOR "+unittest_paths[ix])
      
tester = TestPrintOutput()
tester.test()