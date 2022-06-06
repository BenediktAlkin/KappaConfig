from .tree_nodes import RootNode, InterpolatedNode, FixedNode

class TreeParser:
    @staticmethod
    def parse(value):
        root_node = RootNode()
        TreeParser._parse(value, root_node)
        return root_node

    @staticmethod
    def _parse(value, parent_node):
        if not isinstance(value, str):
            raise TypeError

        while True:
            if len(value) == 0:
                return
            if "${" not in value:
                parent_node.children.append(FixedNode(value))
                return

            brace_start = value.index("${")
            if brace_start != 0:
                parent_node.children.append(FixedNode(value[:brace_start]))
            value = value[brace_start + 2:]
            brace_end = TreeParser._find_brace_end(value)

            value_in_braces = value[:brace_end]
            if ":" in value_in_braces:
                colon_idx = value_in_braces.index(":")
                if colon_idx == 0:
                    raise ValueError
                else:
                    node = InterpolatedNode(value_in_braces[:colon_idx])
            else:
                node = InterpolatedNode(None)
                colon_idx = -1
            parent_node.children.append(node)


            # parse recursively
            TreeParser._parse(value[colon_idx+1:brace_end], node)
            value = value[brace_end+1:]


    @staticmethod
    def _find_brace_end(value):
        nesting_level = 1
        for i in range(len(value)):
            if value[i] == "}":
                nesting_level -= 1
                if nesting_level == 0:
                    return i
            if value[i] == "$" and i != len(value) - 2 and value[i + 1] == "{":
                nesting_level += 1
        raise ValueError