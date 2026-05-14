import csv

def load_controls(filename='Media/controls.csv'):
    """ 
    Loads the control settings from a CSV file and returns them as a dictionary.

    The CSV file (default: 'Media/controls.csv') has the following structure:
    key,axis,no_modifier,ctrl,alt
    U,x,rotate_pos,translate_pos,scale_pos
    J,x,rotate_neg,translate_neg,scale_neg
    ...

    Each row represents a key and its associated actions:
    - 'key': The keyboard key
    - 'axis': The axis affected (x, y, z)
    - 'no_modifier': Action when key is pressed alone
    - 'ctrl': Action when pressed with Ctrl
    - 'alt': Action when pressed with Alt

    Args:
        filename (str, optional): Path to the controls CSV file. 

    Returns:
        dict: A dictionary of control settings.
    """
    controls = {}
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            controls[row['key']] = {
                'axis': row['axis'],
                'no_modifier': row['no_modifier'],
                'ctrl': row['ctrl'],
                'alt': row['alt']
            }
    return controls
