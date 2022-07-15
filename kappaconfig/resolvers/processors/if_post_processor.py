from .processor import Processor


class IfPostProcessor(Processor):
    def __init__(self, allow_empty_result=False):
        self.allow_empty_result = allow_empty_result

    def preorder_process(self, node, trace, **_):
        if isinstance(node, dict) and "if" in node:
            if not node["if"]:
                i = 1
                while True:
                    parent, parent_accessor = trace[-i]
                    # not sure if replacing .pop with del has unwanted behaviour here
                    # with .pop the postprocessing can still be done for the removed node even though it is useless
                    # maybe del would be slightly faster but result in some error
                    parent.pop(parent_accessor)
                    if self.allow_empty_result:
                        break
                    if len(parent) > 0:
                        break
                    # if len(parents) == 0 --> remove parent node as well (this avoids empty dicts/lists)
                    i += 1
                    if i > len(trace):
                        # special case when everything is removed --> replace empty dict with None
                        if len(parent) == 0:
                            parent[parent_accessor] = None
                        break
