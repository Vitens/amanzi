import ast
import math

class VariableVisitor(ast.NodeVisitor):
    def __init__(self):
        self.variables = set()

    def visit_Name(self, node):
        self.variables.add(node.id)
        self.generic_visit(node)

class Output:
    def __init__(self, name, section, category, namespace, param, indent=False):
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
        self.indent = indent

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

    def _parse_expression(self, expression):
        """
        Parse the equation using AST to extract variables and compile it for evaluation.
        """
        try:
            expression = ast.parse(expression, mode='eval')
            compiled = compile(expression, '<string>', 'eval')
        except Exception as e:
            raise ValueError(f"Invalid equation syntax for {self.name}: {e}")
        
        return expression, compiled

    def _extract_dependencies(self, expression):
        """
        Extract variable names from the parsed expression that are not built-ins or library names.
        
        :return: A set of dependencies
        """
        visitor = VariableVisitor()
        visitor.visit(expression)
        dependencies = visitor.variables - set(self.allowed_builtins.keys()) - set(self.allowed_libraries.keys())
        return dependencies
    
    def calculate(self, context, evaluation_stack=None):
        """
        Calculate the expression using the given context.

        :param context: Dictionary containing variable values needed for evaluation
        :return: Evaluated result
        :raises ValueError: If a dependency is missing in the context
        """
        if self.value is not None:
            return self.value
        self.value = self._calculate_expression(self.param['equation'], context,evaluation_stack=evaluation_stack)
        return self.value

    def _calculate_expression(self, expression, context, evaluation_stack=None):
        """
        Calculate the expression using the given context. If already evaluated, return the cached value.

        :param context: Dictionary containing variable values needed for evaluation
        :return: Evaluated result
        :raises ValueError: If a dependency is missing in the context
        """

        expression, compiled = self._parse_expression(expression)
        # extract dependencies
        dependencies = self._extract_dependencies(expression)

        if evaluation_stack is None:
            evaluation_stack = []
        
        if self.name in evaluation_stack:
            raise ValueError(f"Circular reference detected for {self.name}, stack: {evaluation_stack}")
        
        evaluation_stack.append(self.name)

        # Create a context for evaluation with allowed built-ins and libraries
        ctx = {"__builtins__": self.allowed_builtins} | self.allowed_libraries

        for d in dependencies:
            if d not in context:
                raise ValueError(f"Variable '{d}' not found in context for {self.name}")

            if isinstance(context[d], Output):
                ctx[d] = context[d].calculate(context, evaluation_stack)
            else:
                ctx[d] = context[d]

        try:
            # Evaluate the expression safely
            value = eval(compiled, {'__builtins__': ctx['__builtins__']}, ctx)
        except Exception as e:
            raise ValueError(f"Error evaluating expression \"{self.param['equation']}\" for {self.name}: {e}")
        
        # Remove the current parameter from the stack
        evaluation_stack.pop()

        return value

    def validate(self, context):
        """
        Check if the parameter is valid based on the validation condition if available.

        :return: True if valid, False otherwise
        """
        if 'validation' in self.param:
            return self._calculate_expression(self.param['validation'], context)
        return True
    
    def hidden(self, context):
        """
        Check if the parameter is hidden based on the condition if available.

        :return: True if hidden, False otherwise
        """
        if 'if' in self.param:
            return not self._calculate_expression(self.param['if'], context)
        return False

    @property
    def uom(self):
        """
        Get the unit of measure for the parameter if available.

        :return: Unit of measure or None
        """
        return self.param.get('uom', None)
    
    @property
    def precision(self):
        """
        Get the precision for the parameter if available.

        :return: Precision or None
        """
        return self.param.get('precision', None)

    def reset(self):
        """
        Reset the cached value to allow re-evaluation if needed.
        """
        self.value = None
