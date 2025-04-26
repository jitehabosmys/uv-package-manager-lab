def add(a, b):
    return a + b

def test_add():
    assert add(1, 2) == 3
    assert add(-1, 1) == 0
    assert add(0, 0) == 0

def test_string_methods():
    s = "hello world"
    assert s.upper() == "HELLO WORLD"
    assert s.capitalize() == "Hello world"
    assert s.split() == ["hello", "world"]
    
if __name__ == "__main__":
    print("运行 pytest test_example.py 来执行这些测试") 