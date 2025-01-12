import re


class Utils:
    @staticmethod
    def clean_string(content):
        """
        Generic function to clean and format text content from Databricks responses.
        Handles error traces, JSON strings, and general text with special characters.
        """
        import re

        # If not string, return as is
        if not isinstance(content, str):
            return content

        # Remove ANSI color codes
        ansi_escape = re.compile(r'\x1b\[[0-9;]*[mGKH]')
        content = ansi_escape.sub('', content)

        # Handle escaped characters
        content = content.strip('"\'')  # Remove surrounding quotes
        content = content.replace('\\n', '\n')
        content = content.replace('\\t', '    ')
        content = content.replace('\\"', '"')
        content = content.replace('\\r', '')

        # Remove non-ASCII characters
        content = content.encode('ascii', 'ignore').decode('ascii')

        # Clean extra whitespace but preserve indentation
        lines = content.split('\n')
        cleaned_lines = []
        
        for line in lines:
            # Preserve empty lines after separators
            if line.strip() and all(c == '-' for c in line.strip()):
                cleaned_lines.append(line)
                continue
                
            # Preserve indentation for code and tracebacks
            indent = len(line) - len(line.lstrip())
            cleaned = line.strip()
            if cleaned:
                cleaned_lines.append(' ' * indent + cleaned)

        return '\n'.join(cleaned_lines)


    @staticmethod
    def clean_data(data):
        """Recursively clean all strings in a dictionary."""
        if isinstance(data, dict):
            return {k: Utils.clean_data(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [Utils.clean_data(item) for item in data]
        else:
            return Utils.clean_string(data)
