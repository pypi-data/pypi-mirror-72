from cleverdict import CleverDict
import pytest
import os
from collections import UserDict

def my_example_save_function(self, name: str = "", value: any = ""):
    """
    Example of a custom function which can be called by self._save()
    whenever the value of a CleverDict instance is created or changed.

    Required arguments are: self, name: str and value: any

    Specify this (or any other) function as the default 'save' function as follows:

    CleverDict._save = my_example_save_function
    """
    output=f"Notional save to database: .{name} = {value} {type(value)}"
    print(output)
    with open("example.log","a") as file:
        file.write(output)

class Test_Core_Functionality():
    def test_creation_using_existing_dict(self):
        """ CleverDicts can be creates from existing dictionaries """
        x = CleverDict({'total':6, 'usergroup': "Knights of Ni"})
        assert x.total == 6
        assert x['total'] == 6
        assert x.usergroup == "Knights of Ni"
        assert x['usergroup'] == "Knights of Ni"

    def test_creation_using_existing_UserDict(self):
        """ CleverDicts can be creates from existing UserDict objects """
        u = UserDict({'total':6, 'usergroup': "Knights of Ni"})
        x = CleverDict(u)
        assert x.total == 6
        assert x['total'] == 6
        assert x.usergroup == "Knights of Ni"
        assert x['usergroup'] == "Knights of Ni"

    def test_creation_using_keyword_arguments(self):
        """ CleverDicts can be created using keyword assignment """
        x = CleverDict(created = "today", review = "tomorrow")
        assert x.created == "today"
        assert x['created'] == "today"
        assert x.review == "tomorrow"
        assert x['review'] == "tomorrow"

    def test_creation_using_vars(self):
        """ Works for 'simple' data objects i.e. no methods just data """
        class My_class:
            pass
        m = My_class()
        m.subject = "Python"
        x = CleverDict(vars(m))
        assert x.subject == "Python"
        assert x['subject'] == "Python"


    def test_value_change(self):
        """ New attribute values should update dictionary keys & vice versa """
        x = CleverDict()
        x.life = 42
        x['life'] = 43
        assert x.life == 43
        assert x['life'] == 43
        x.life = 42
        assert x.life == 42
        assert x['life'] == 42

class Test_Save_Functionality():

    def delete_log(self):
        try:
            os.remove("example.log")
        except FileNotFoundError:
            pass

    def test_save_on_creation(self):
        """ Once set, CleverDict._save should be called on creation """
        CleverDict._save = my_example_save_function
        self.delete_log()
        x = CleverDict({'total':6, 'usergroup': "Knights of Ni"})
        with open("example.log","r") as file:
            log = file.read()
        assert log == "Notional save to database: .total = 6 <class 'int'>Notional save to database: .usergroup = Knights of Ni <class 'str'>"
        self.delete_log()

    def test_save_on_update(self):
        """ Once set, CleverDict._save should be called after updates """
        x = CleverDict({'total':6, 'usergroup': "Knights of Ni"})
        self.delete_log()
        CleverDict._save = my_example_save_function
        x.total += 1
        with open("example.log","r") as file:
            log = file.read()
        assert log == "Notional save to database: .total = 7 <class 'int'>"
        self.delete_log()

class Test_normalise():

    def test_normalise(self):
        """
        Object attributes can't be empty, must start with a letter, and can
        only contain numbers, letters or "_".

        By default, CleverDict will attempt to normalise attribute names.
        """
        assert CleverDict.normalise
        testcases = {2: "_2",
                     None: "None",
                     True: "True",
                     False: "False",
                     "": "_nullstring",
                     " ": "_space",
                     "two words": "two_words",
                     "#punctuation?'!;,": "_punctuation_____"}
        for testcase, expected_result in testcases.items():
            x = CleverDict({testcase: "whatever"})
            assert hasattr(x,expected_result)

    def test_normalise_disabled(self):
        CleverDict.normalise = False
        testcases = {2: "_2",
                "": "_nullstring",
                " ": "_space",
                "two words": "two_words",
                "#punctuation?'!;,": "_punctuation_____"}
        for testcase, expected_result in testcases.items():
            x = CleverDict({testcase: "whatever"})
            assert not hasattr(x,expected_result)
            assert x.get(testcase)
            assert not x.get(expected_result)
        CleverDict.normalise = True

class MyClass(CleverDict):
    def __init__(self,id):
        self.id = id
