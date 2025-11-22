import re

def sanskrit_interpreter(code):
    # Function to replace Sanskrit numerals with standard numerals
    def replace_sanskrit_numerals(s):
        sanskrit_to_arabic = {
            '०': '0', '१': '1', '२': '2', '३': '3', '४': '4',
            '५': '5', '६': '6', '७': '7', '८': '8', '९': '9'
        }
        for sanskrit_num, arabic_num in sanskrit_to_arabic.items():
            s = s.replace(sanskrit_num, arabic_num)
        return s

    # Define Sanskrit command patterns
    patterns = {
        r'लिखतु\("(.*?)"\);': lambda match: print(match.group(1)),  # Print function
        r'([\wअ-ह]+)\s*=\s*(.*?);': lambda match: variables.update({match.group(1): replace_sanskrit_numerals(match.group(2))})  # Variable assignment
    }

    variables = {}
    lines = code.split('\n')

    # First pass: Handle variable assignments
    for line in lines:
        line = line.strip()
        for pattern, action in patterns.items():
            match = re.match(pattern, line)
            if match:
                action(match)

    # Function to manually evaluate condition with replaced variables
    def evaluate_condition(condition_str):
        # Replace Sanskrit variables with their values in the condition string
        condition_str = replace_sanskrit_numerals(condition_str)
        for var, value in variables.items():
            condition_str = condition_str.replace(var, str(value))  # Replace with actual value
        try:
            # Evaluate the modified condition string
            if condition_str:
                return eval(condition_str)
            return False
        except Exception as e:
            print(f"Error in condition evaluation: {e}")
            return False

    # Second pass: Evaluate conditions
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        executed = False
        if line.startswith("यदि"):
            condition = re.match(r'यदि \((.*?)\):', line)
            if condition:
                condition_eval = condition.group(1)
                # Evaluate the condition using the custom evaluate_condition function
                if evaluate_condition(condition_eval):
                    i += 1
                    line = lines[i].strip()
                    match = re.match(r'लिखतु\("(.*?)"\);', line)
                    if match:
                        print(match.group(1))
                else:
                    i += 2  # Skip 'अन्यथा:' block
        elif line.startswith("अन्यथा:"):
            i += 1
            line = lines[i].strip()
            match = re.match(r'लिखतु\("(.*?)"\);', line)
            if match:
                print(match.group(1))
        elif not executed and line.strip():
            print(f"अज्ञात आदेश: {line}")
        i += 1

# Sample Sanskrit Code
sanskrit_code = """
संख्या = ५ + ५;
यदि (संख्या > ५):
    लिखतु("संख्या बड़ी है");
अन्यथा:
    लिखतु("संख्या छोटी है");
"""

sanskrit_interpreter(sanskrit_code)
