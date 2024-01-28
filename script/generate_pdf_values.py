# pylint: skip-file
"""Regenerate pdf values after experiment execution"""
from evaluate import show_analysis

FILE_PATH = '/home/kali/JSONSchemaDiscovery/ReproEngReport/main.tex'

def generate_latex_values():
    # Open the file in read and write mode
    with open(FILE_PATH, 'r+') as file:
        # Read the content of the LaTeX template
        latex_template = file.read()

        # List of values to be inserted into the LaTeX template
        list_of_values = show_analysis()
        
        # Initialize the rows string
        rows = ''

        # Iterate over the list_of_values and build rows
        for values in list_of_values:
            row = f"{values['collectionName']} & {values['collectionCount']} & {values['uniqueUnorderedCount']} & {values['uniqueOrderedCount']} \\\\"
            rows += row + '\n'  # Ensure a new line after each row
            rows += '\hline\n'  # Add \hline after each row

        # Replace %ROWS% with the generated rows in the LaTeX template
        latex_template = latex_template.replace('%ROWS%', rows)

        # Set the file position back to the beginning
        file.seek(0)

        # Write the modified LaTeX template back to the file
        file.write(latex_template)

if __name__ == '__main__':
    generate_latex_values()