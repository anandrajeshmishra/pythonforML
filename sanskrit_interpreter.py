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
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        executed = False
        for pattern, action in patterns.items():
            match = re.match(pattern, line)
            if match:
                action(match)
                executed = True
                break
        if line.startswith("यदि"):
            condition = re.match(r'यदि \((.*?)\):', line)
            if condition:
                condition_eval = replace_sanskrit_numerals(condition.group(1))
                for var in variables:
                    condition_eval = condition_eval.replace(var, str(variables[var]))
                if eval(condition_eval):
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
