import pytest
def test__example_func():
    assert 34 == 34

def test_isInstance():
    assert isinstance('hello world',str)
    assert not isinstance(12,str)

def test_bool():
    validated = True
    assert validated is True
    assert False is not True

def test_greater_than_less_than():
    assert 12 > 9
    assert 9 < 24

def test_list():
    num_list = [4,6,23,423,6,2]
    bool_list = [False, True, False, True]

    assert 4 in num_list
    assert 7 not in num_list
    assert False in bool_list and True in bool_list 

class Student:
    def __init__(self,first_name:str, last_name:str, major:str, year:int):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.year = year

    def __str__(self):
        return f"{self.first_name} {self.last_name} \n{self.major}\n{self.year}"

@pytest.fixture
def person():
    return Student('Johnny','Doeee','Computer Sci.',2)

def test_person(person):
    
    assert person.first_name == 'Johnny', 'First name should be Johnny'
    assert person.last_name == 'Doeee', 'Last name should be Doeee'
    assert person.major == 'Computer Sci.', 'Major should be Computer Sci.'
    assert person.year == 2,'Year should be' + ' ' + 2