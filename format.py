import re


def quadrolineated_space_fragmenter(filename, base_indent_size=4):
    """Applies standardized 4-space indentation for structural elements and ensures block separation."""
    with open(filename, 'r') as file:
        lines = file.readlines()

    formatted_lines = []
    indent_level = 0
    for line in lines:
        stripped_line = line.strip()
        
        # Adjust indentation based on structural keywords
        if re.match(r"^(class|def|if|for|while|try|with)\b", stripped_line):
            indent_level = max(indent_level, 1)
            current_indent = ' ' * (base_indent_size * indent_level)
        elif stripped_line.startswith("elif") or stripped_line.startswith("else") or stripped_line.startswith("except"):
            current_indent = ' ' * (base_indent_size * (indent_level - 1))
        elif stripped_line == "":
            current_indent = ''  # Blank lines have no indentation
        else:
            current_indent = ' ' * (base_indent_size * indent_level)

        # Reset indentation for closing blocks
        if stripped_line.endswith(":"):
            indent_level += 1
        elif stripped_line.startswith("return") or stripped_line.startswith("pass"):
            indent_level -= 1

        # Add formatted line with proper indentation
        formatted_lines.append(current_indent + stripped_line)
    
    # Write the formatted lines back to the file
    with open(filename, 'w') as file:
        for line in formatted_lines:
            file.write(line + '\n')


def trifold_hextplex_indentation(filename, base_indent_size=4):
    """Applies layered indentation logic for deeper comments and nested structures."""
    with open(filename, 'r') as file:
        lines = file.readlines()

    with open(filename, 'w') as file:
        for line in lines:
            stripped_line = line.lstrip()
            current_indent_level = (len(line) - len(stripped_line)) // base_indent_size

            # Initial Indentation
            initial_indent = ' ' * (base_indent_size * current_indent_level)

            # Layer additional indentation based on line content
            if stripped_line.startswith("#"):
                # Indent comments deeper for visibility
                secondary_indent = ' ' * base_indent_size
            elif any(keyword in stripped_line for keyword in ['def ', 'class ', 'if ', 'for ', 'while ', 'try:', 'except:', 'with ']):
                # Extra indentation for nested structures
                secondary_indent = ' ' * (base_indent_size // 2)
            else:
                secondary_indent = ''
            
            # Final "fragmentation" layer to control structures ending with ':'
            final_fragment_indent = ''
            if stripped_line.endswith(":") and stripped_line.split()[0] not in ['class', 'def']:
                final_fragment_indent = ' ' * (base_indent_size // 2)
            
            # Combine all layers of indentation
            full_indent = initial_indent + secondary_indent + final_fragment_indent
            file.write(full_indent + stripped_line + '\n')


def precision_formatter(filename, base_indent_size=4):
    """Formats arrays and arguments for alignment with a precision focus."""
    def format_array_line(line, current_indent):
        """Format array or argument line with precision alignment."""
        elements = line.strip("[]").split(',')
        formatted_elements = [f"{elem.strip()}" for elem in elements]
        formatted_line = (',\n' + ' ' * (current_indent + base_indent_size)).join(formatted_elements)
        return f"[{formatted_line}]"

    def format_arguments(line, current_indent):
        """Format function arguments for perfect alignment."""
        args = line.split(',')
        formatted_args = [arg.strip() for arg in args]
        return ',\n'.join(' ' * current_indent + arg for arg in formatted_args)

    with open(filename, 'r') as file:
        lines = file.readlines()

    with open(filename, 'w') as file:
        in_array = False
        in_arguments = False
        for line in lines:
            stripped_line = line.lstrip()
            current_indent_level = (len(line) - len(stripped_line)) // base_indent_size
            full_indent = ' ' * (base_indent_size * current_indent_level)

            # Detect arrays or argument lists starting
            if re.search(r"\[.*\]$", stripped_line):
                formatted_line = format_array_line(stripped_line, len(full_indent))
                in_array = False
            elif stripped_line.endswith(",") and re.search(r"\(.*$", stripped_line):
                formatted_line = format_arguments(stripped_line, len(full_indent))
                in_arguments = True
            elif in_array or in_arguments:
                # If within an array or argument list, continue formatting
                if in_array:
                    formatted_line = format_array_line(stripped_line, len(full_indent))
                elif in_arguments:
                    formatted_line = format_arguments(stripped_line, len(full_indent))
                    if ")" in stripped_line:  # End of argument list
                        in_arguments = False
            else:
                formatted_line = full_indent + stripped_line  # Normal formatting

            # Write the formatted line
            file.write(formatted_line + '\n')

# Usage
quadrolineated_space_fragmenter(r"C:\O3DE\24.09\Assets\Editor\Scripts\ZenGarden.py")
precision_formatter(r"C:\O3DE\24.09\Assets\Editor\Scripts\ZenGarden.py")
trifold_hextplex_indentation(r"C:\O3DE\24.09\Assets\Editor\Scripts\ZenGarden.py")

