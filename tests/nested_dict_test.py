test_dict = {
    "test1" : {"Nested1" : 1},
    "test2" : {"Nested2" : 2},
    "test3" : {"Nested3" : 3}
}

for key, value in test_dict.items():
    for i in value.keys():
        print(i)