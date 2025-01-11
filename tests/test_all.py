if True: import sys; sys.path.append('.') # needed to run this file


def test_all():
    all_paths = sys.path.copy()
    
    from sysappend import all
    all()
    
    assert sys.path != all_paths
    

if __name__ == '__main__':
    import inspect
    
    def run_all_tests():
        for name, obj in inspect.getmembers(sys.modules[__name__]):
            if inspect.isfunction(obj) and name.startswith('test_'):
                print(f"Running {name}...")
                obj()

    run_all_tests()
    
    
    
