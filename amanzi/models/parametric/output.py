import ast
import math

class VariableVisitor(ast.NodeVisitor):
    def __init__(self):
        self.variables = set()

    def visit_Name(self, node):
        self.variables.add(node.id)
        self.generic_visit(node)

class Output:
    def __init__(self, name, section, category, namespace, param):
        """
        Initialize the Output object with metadata, parameter information, and dependencies.

        :param name: Name of the parameter
        :param section: Section the parameter belongs to
        :param category: Category the parameter belongs to
        :param namespace: Namespace the parameter belongs to
        :param param: Dictionary containing parameter details including the equation
        """
        self.name = name
        self.section = section
        self.category = category
        self.namespace = namespace
        self.param = param

        # Cached value for the evaluated expression
        self.value = None

        # Allowed built-ins and libraries for expression evaluation
        self.allowed_builtins = {
            'abs': abs,
            'max': max,
            'min': min,
            'round': round,
            'sum': sum,
        }
        self.allowed_libraries = {
            'math': math,
        }

        # Parse the expression and extract dependencies
        self._parse_expression()
        self.dependencies = self._extract_dependencies()

    def _parse_expression(self):
        """
        Parse the equation using AST to extract variables and compile it for evaluation.
        """
        try:
            self.expression = ast.parse(self.param['equation'], mode='eval')
            self.compiled = compile(self.expression, '<string>', 'eval')
        except Exception as e:
            raise ValueError(f"Invalid equation syntax for {self.name}: {e}")

    def _extract_dependencies(self):
        """
        Extract variable names from the parsed expression that are not built-ins or library names.
        
        :return: A set of dependencies
        """
        visitor = VariableVisitor()
        visitor.visit(self.expression)
        dependencies = visitor.variables - set(self.allowed_builtins.keys()) - set(self.allowed_libraries.keys())
        return dependencies

    def evaluate(self, context, evaluation_stack=None):
        """
        Evaluate the expression using the given context. If already evaluated, return the cached value.

        :param context: Dictionary containing variable values needed for evaluation
        :return: Evaluated result
        :raises ValueError: If a dependency is missing in the context
        """
        if self.value is not None:
            return self.value
        
        if evaluation_stack is None:
            evaluation_stack = []
        
        if self.name in evaluation_stack:
            raise ValueError(f"Circular reference detected for {self.name}, stack: {evaluation_stack}")
        
        evaluation_stack.append(self.name)

        # Create a context for evaluation with allowed built-ins and libraries
        ctx = {"__builtins__": self.allowed_builtins} | self.allowed_libraries

        for d in self.dependencies:
            if d not in context:
                raise ValueError(f"Variable '{d}' not found in context for {self.name}")

            if isinstance(context[d], Output):
                ctx[d] = context[d].evaluate(context, evaluation_stack)
            else:
                ctx[d] = context[d]

        try:
            # Evaluate the expression safely
            self.value = eval(self.compiled, {'__builtins__': ctx['__builtins__']}, ctx)
        except Exception as e:
            import pprint
            pprint.pprint(ctx)
            raise ValueError(f"Error evaluating expression \"{self.param['equation']}\" for {self.name}: {e}")
        
        # Remove the current parameter from the stack
        evaluation_stack.pop()

        return self.value

    @property
    def uom(self):
        """
        Get the unit of measure for the parameter if available.

        :return: Unit of measure or None
        """
        return self.param.get('uom', None)

    def reset(self):
        """
        Reset the cached value to allow re-evaluation if needed.
        """
        self.value = None
