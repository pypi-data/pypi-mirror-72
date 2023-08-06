def row_string(fixed, size, row, col_sep='|', padding=0):
    """
    Converts a dict of fixed cells to a string.

    fixed - a cell-symbol dictionary
    size - the dimension of the PLS
    row - the row to convert to a string
    col_sep - a string used as a separator between columns
    padding - number of spaces either side of a symbol
    """
    s = col_sep
    for col in range(size):
        symbol = fixed.get(cell(row, col, size))
        if symbol:
            s += ' '*padding + str(symbol)
        else:
            s += ' '*padding + '.'   
        s += col_sep
    return s

def dict_to_string(fixed, size, col_sep = '', row_sep = '', padding = 0, top = '', bottom = ''):
    """
    Returns a puzzle string of dimension 'boxsize' from a dictionary of 
    'fixed' cells.
    
    padding : number of spaces between adjacent symbols
    row_end : a string added to the last symbol of every row 
    col_sep : a string added to the last symbol of every column
    
    """
    rows = range(size)
    s = top
    for row in rows[:-1]:
        s += row_string(fixed, size, row, col_sep, padding)
        s += row_sep
    s += row_string(fixed, size, rows[size-1], col_sep, padding)
    s += ' '*padding
    s += bottom
    return s

def dict_to_string_simple(fixed, size):
    return dict_to_string(fixed, size, col_sep = '|', row_sep = '\n', padding = 0, top = '', bottom = '')

def cell(row, column, size):
    """The label of the cell in position (row, col)."""
    return (row * size) + column + 1

def row(cell, size): 
    """The row label of the row in a square of dimension 'size'
    containing the cell with label 'cell'."""
    return int((cell - 1)/size) 

def col(cell, size): 
    """The column label of the column in a square of dimension 'size'
    containing the cell with label 'cell'."""
    return (cell - 1) % size

def row_r(cell, size): 
    """A range of all labels of cells in the same row as 'cell'."""
    return range(row(cell, size)*size + 1, (row(cell, size) + 1)*size + 1)

def col_r(cell, size): 
    """A range of all labels of cells in the same column as 'cell'."""
    return range(col(cell, size) + 1, size**2 + 1, size)

def vertex(cell, size):
    """The row and column labels of 'cell', as a pair."""
    return (row(cell, size), col(cell, size))

def rect_r(tl, br, size):
    """A rectangular range which extends from tl in the top-left to br in the
    bottom right."""
    (i,j) = vertex(tl, size)
    (k,l) = vertex(br, size)
    cells = [(x, y) for x in range(i, k + 1) for y in range(j, l + 1)]
    return map(lambda x: cell(x[0], x[1], size), cells)

def list_assignment(partial_latin_square, size):
    """The (canonical) list assignment for a partial latin square. The list of
    a filled cell is the list containing just the element in that cell. The
    list of an empty cell contains only those symbols not already used in the
    same row and column as that cell."""
    P = partial_latin_square
    L = {}
    # initialise lists
    for i in range(1, size**2 + 1):
        if i in P.keys():
            L[row(i,size),col(i,size)] = [P[i]]
        else:
            L[row(i,size),col(i,size)] = range(1, size + 1)
    # update lists (remove used symbols from lists of same row/col)
    for i in range(1, size**2 + 1):
        if i in P.keys():
            # then remove P[i] from any list of a cell not in P from the same row/col
            for j in row_r(i, size) + col_r(i, size):
                if j not in P.keys():
                    if P[i] in L[row(j, size), col(j, size)]:
                        L[row(j, size), col(j, size)].remove(P[i])
    return L

def orthogonal_array(L, size):
    return [(i,j,L[i,j]) for i,j in range(size)]

def sim_2_csm(P, size):
    """Fixed cells from a list colouring.

    Convert a symbols-to-(row,col) pairs dictionary to a cell-label-to-symbol
    dictionary.
    """
    L = {}
    for i in P:
        for j in P[i]:
            row = j[0]
            column = j[1]
            L[cell(row, column, size)] = int(i)
    return L

def com_2_csm(P, size):
    """Fixed cells from a list of row dictionaries.

    Convert a list of column-labels-to-symbols dictionaries to a
    cell-label-to-symbol dictionary.
    """
    L = {}
    for i in range(len(P)):
        for j in P[i]:
            if P[i][j] != '.':
                row = i
                col = j
                L[cell(row, col, size)] = int(P[i][j])
    return L

class Latin:

    def __init__(self, P, size, symbols = None, format = ''):
        self._size = size
        if symbols == None:
            self._symbols = range(1, size + 1)
        else:
            self._symbols = symbols
        if format == 'sim':
            self._P = sim_2_csm(P, size)
        elif format == 'com':
            self._P = com_2_csm(P, size)
        else:
            self._P = P

    def __repr__(self):
        return dict_to_string_simple(self._P, self._size)

    def __str__(self):
        return self.__repr__()

    def __getitem__(self, key):
        return self._P[cell(key[0], key[1], self._size)]

    def size(self):
        return self._size

    def symbols(self):
        return self._symbols

    def row_presences(self, row_index):
        result = []
        first_cell = cell(row_index, 1, self._size)
        row = row_r(first_cell, self._size)
        for cell_ in row:
            symbol = self._P.get(cell_)
            if symbol!=None:
                result.append(symbol)
        return result

    def row_absences(self, row_index):
        result = self.symbols()[:]
        presences = self.row_presences(row_index)
        for x in presences:
            if x in result:
               result.remove(x)
        return result

    def fixed_cells(self):
        return self._P

    def extend(self, disjoint_fixed):
        self._P.update(disjoint_fixed)

