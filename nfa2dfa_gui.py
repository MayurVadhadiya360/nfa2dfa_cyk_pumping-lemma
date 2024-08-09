import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import pandas as pd
import numpy as np
import math


class FA:
    def __init__(self, csv_file_path):
        self.NFA = None
        self.DFA = None
        self.DFA_state_table = None
        self.NFA_state_table = None
        self.csv_file_path = csv_file_path
        self.NFA = self.nfa_from_table()

    def nfa_from_table(self):
        nfa_table = pd.read_csv(self.csv_file_path)
        self.NFA_state_table = nfa_table

        #     print(nfa_table)
        """
        Convert an NFA represented as a Pandas DataFrame in state table format to a dictionary.
        The DataFrame should have columns 'State', '0', and '1' (or whatever input symbols are used).
        Returns a dictionary with keys 'states', 'alphabet', 'transitions', 'start_state', and 'accepting_states'.
        """
        # Extract states from the first column of the DataFrame
        states = set(nfa_table['State'])

        # Extract alphabet from the column names of the DataFrame
        alphabet = set(nfa_table.columns[1:-1])

        # Build transitions dictionary from the DataFrame
        transitions = {}
        for row in nfa_table.itertuples():
            state = row.State
            for symbol in alphabet:
                dest_states_str = getattr(row, symbol)
                if isinstance(dest_states_str, float) and math.isnan(dest_states_str):
                    dest_states = set()  # treat NaN values as empty cells
                elif dest_states_str:
                    dest_states = set(dest_states_str.split(','))
                else:
                    dest_states = set()
                transitions[(state, symbol)] = dest_states

        # Extract start state from the first row of the DataFrame
        start_state = nfa_table['State'][0]

        # Extract accepting states from rows where 'Accepting' column is True
        accepting_states = set(nfa_table.loc[nfa_table['Accepting'], 'State'])

        return {
            'states': states,
            'alphabet': alphabet,
            'transitions': transitions,
            'start_state': start_state,
            'accepting_states': accepting_states
        }

    def nfa_to_dfa(self):
        nfa = self.NFA
        """
        Convert an NFA represented as a dictionary to a DFA using the subset construction algorithm.
        The NFA should have keys 'states', 'alphabet', 'transitions', 'start_state', and 'accepting_states'.
        Returns a DFA represented as a dictionary with the same keys.
        """
        dfa = {
            'states': set(),
            'alphabet': nfa['alphabet'],
            'transitions': {},
            'start_state': frozenset([nfa['start_state']]),
            'accepting_states': set()
        }

        queue = [dfa['start_state']]
        processed = set()

        while queue:
            current_state = queue.pop(0)
            if current_state in processed:
                continue
            processed.add(current_state)

            dfa['states'].add(current_state)
            if any(state in nfa['accepting_states'] for state in current_state):
                dfa['accepting_states'].add(current_state)

            for symbol in dfa['alphabet']:
                next_states = set()
                for state in current_state:
                    next_states |= set(nfa['transitions'].get((state, symbol), []))
                next_state = frozenset(next_states)
                if not next_state:
                    next_state = frozenset([''])
                dfa['transitions'][(current_state, symbol)] = next_state
                if next_state not in processed:
                    queue.append(next_state)

        self.DFA = dfa
        return dfa

    def dfa_to_table(self):
        dfa = self.DFA
        """
        Convert a DFA represented as a dictionary to a Pandas DataFrame in state table format.
        The DFA should have keys 'states', 'alphabet', 'transitions', 'start_state', and 'accepting_states'.
        Returns a Pandas DataFrame with columns 'State', 'Accepting', '0', '1', etc. (one column for each input symbol).
        """
        # Build a list of rows for the DataFrame
        rows = []
        for state in dfa['states']:
            row = {'Accepting': state in dfa['accepting_states'], 'State': ",".join(state)}
            for symbol in dfa['alphabet']:
                next_state = dfa['transitions'].get((state, symbol))
                if next_state:
                    row[symbol] = ",".join(next_state)
                else:
                    row[symbol] = ''
            rows.append(row)

        # Sort rows by state name and convert to DataFrame
        df = pd.DataFrame(rows).sort_values('State').reset_index(drop=True)
        self.DFA_state_table = df
        return df


# if __name__ == "__main__":
#     nfa = {
#         'states': {'q0', 'q1', 'q2'},
#         'alphabet': {'0', '1'},
#         'transitions': {
#             ('q0', '0'): {'q0', 'q1'},
#             ('q0', '1'): {'q1'},
#             ('q1', '0'): {'q2'},
#             ('q1', '1'): {'q2'},
#             ('q2', '0'): {'q0', 'q1'},
#             ('q2', '1'): {'q1', 'q2'}
#         },
#         'start_state': 'q0',
#         'accepting_states': {'q1', 'q2'}
#     }
#
#     fa = FA("nfa2.csv")
#     fa.nfa_to_dfa()
#     fa.dfa_to_table()
#     print(fa.NFA_state_table)
#     print(fa.DFA_state_table)
#     # print(list(fa.DFA_state_table))
#     # print(fa.DFA_state_table.values.tolist())


def select_csv():
    try:
        file_path = filedialog.askopenfilename(filetypes=[('CSV', '*.csv')])
        fa = FA(file_path)
        fa.nfa_to_dfa()
        fa.dfa_to_table()
        # print(fa.DFA_state_table)
        show_table(fa.NFA_state_table, "NFA")
        show_table(fa.DFA_state_table, "DFA")
    except Exception as e:
        print("Select proper csv file", f"\n{e}")


def show_table(df, name):
    columns = list(df)
    data = df.values.tolist()
    # Define the table data
    #     data = [('q0', 'q0,q1', 'q0', False),
    #             ('q1', 'q2', '', False),
    #             ('q2', '', '', True)]

    # Create a Tkinter window
    global root
    # rt = tk.Tk()
    # rt.title(name)
    # Create a Treeview widget
    # table = ttk.Treeview(root, columns=("state", 'a', 'b', 'Accepting'), show='headings')
    # tk.Label(text=name).pack()
    table = ttk.Treeview(root, columns=columns, show='headings')
    for i in columns:
        table.heading(i, text=i)
    # table.heading('state', text='State')
    # table.heading('a', text='a')
    # table.heading('b', text='b')
    # table.heading('Accepting', text='Accepting')

    # Insert data into the Treeview
    for row in data:
        table.insert('', 'end', values=row)

    # Pack the Treeview widget
    table.pack(expand=True, fill='both')

    # Start the Tkinter event loop
    # rt.mainloop()


def run():
    global root
    root = tk.Tk()
    root.title("NFA to DFA")
    root.geometry("1000x500")
    select_button = tk.Button(
        root,
        text='Select CSV',
        command=select_csv,
        width=25,
        bg='blue',
        activebackground='black',
        foreground='white'
    )
    select_button.pack()
    root.mainloop()


global root

# run()
# if __name__ == "__main__":
#     global root
#     root = tk.Tk()
#     root.title("NFA to DFA")
#     select_button = tk.Button(root, text='Select CSV', command=select_csv)
#     select_button.pack()
#     root.mainloop()
