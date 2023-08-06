import json

def query_json(dictionary: dict, key, value) -> dict:
    target_records = query_json_with_func(dictionary, lambda x: x[key] == value)
    return target_records

def query_json_with_func(dictionary: dict, func) -> filter:
    target_records = filter(func, dictionary)
    return target_records

class JsonResponseInterpreter:

    """
    Class to assist in easy analysis and interpretation of JSON returned
    from API queries

    Parameter:
    requestResponse (requests response object): http 200 response received
    from the server
    """

    def __init__(self, requestResponse):
        """
        Turns a request response 200 into a usable dictionary
        Executes function parse_json_response to create .jsonDict attribute.
        """
        self.requestResponseText = requestResponse.text
        self.parse_json_response()

    def parse_json_response(self):
        """
        Parses self.requestResponseText into attribute .jsonDict
        """
        self.jsonDict = json.loads(self.requestResponseText)
        self.jsonRoot = self.jsonDict.keys()

    def json_tree_traverse(self, tree_traverse_keys: list):
        """
        Recurses through self.jsonDict treating tree_traverse_keys as a series
        of dictionary keys

        tree_traverse_keys: list
        The series of dictionary keys that you want to use to traverse the
        JSON dictionary

        Will raise KeyError if the list is not in the correct order to traverse
        the dictionary.

        returns: any type (depends on what is at the node / leaf where the
        traverse_keys stop)
        """

        #Enusure you don't hit recursionerror
        assert len(tree_traverse_keys)<=1000, "Too many levels in tree_traverse_keys"

        tree_traverse_keys = iter(tree_traverse_keys)
        localTree = self.jsonDict.copy()

        def get_next_level(remaining_keys, tree):
            """
            Recursive function to traverse the dictionary to find the level
            implied by the tree_traverse_keys argument of parent function
            json_tree_traverse.
            """

            next_level_key = next(remaining_keys, None)
            if next_level_key is None:
                return tree
            else:
                tree = tree[next_level_key]
                return get_next_level(remaining_keys, tree)

        return get_next_level(tree_traverse_keys,localTree)
