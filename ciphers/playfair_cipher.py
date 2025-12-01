"""
Playfair Cipher Implementation
Classical digraph substitution cipher using a 5x5 matrix
"""
class PlayfairCipher:
    def __init__(self, key=None, matrix=None):
        """Initialize cipher either from a key or an explicit 5x5 matrix."""
        if matrix is not None:
            # If given a matrix, skip key processing
            self.matrix = matrix
            self.key = ""
        else:
            # Normalize key: ensure uppercase and merge J->I
            self.key = (key or "").upper().replace("J", "I")
            self.matrix = self._create_matrix()

    def _create_matrix(self):
        """Construct the 5x5 key matrix using the processed key."""
        # Playfair uses a 25-letter alphabet: J removed, merged with I
        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        used = []  # ordered list of characters to form the matrix

        # Insert key letters first, ignoring duplicates and non-letters
        for c in self.key:
            if c.isalpha() and c not in used:
                used.append(c)

        # Append remaining alphabet letters not already included by the key
        for c in alphabet:
            if c not in used:
                used.append(c)

        # Split into 5 rows of 5 columns each
        matrix = []
        for i in range(5):
            row = used[i*5 : (i+1)*5]
            matrix.append(row)

        return matrix

    def _find_position(self, char):
        """Return (row, col) for the given character inside the matrix."""
        for i, row in enumerate(self.matrix):
            for j, c in enumerate(row):
                if c == char:
                    return i, j
        return None

    def _prepare_text(self, text):
        """Normalize and split text into digraphs according to Playfair rules."""
        text = text.upper().replace('J', 'I').replace(' ', '')
        prepared = ""
        
        i = 0
        while i < len(text):
            if not text[i].isalpha():
                i += 1
                continue
            
            prepared += text[i]
            
            if i + 1 < len(text):
                if text[i] == text[i + 1]:
                    prepared += 'X'
                else:
                    prepared += text[i + 1]
                    i += 1
            else:
                prepared += 'X'
            
            i += 1
        
        return prepared

    def encrypt(self, plaintext):
        """Encrypt digraphs according to Playfair transformation rules."""
        plaintext = self._prepare_text(plaintext)
        ciphertext = ""
        
        for i in range(0, len(plaintext), 2):
            row1, col1 = self._find_position(plaintext[i])
            row2, col2 = self._find_position(plaintext[i + 1])
            
            if row1 == row2:  # Same row
                ciphertext += self.matrix[row1][(col1 + 1) % 5]
                ciphertext += self.matrix[row2][(col2 + 1) % 5]
            elif col1 == col2:  # Same column
                ciphertext += self.matrix[(row1 + 1) % 5][col1]
                ciphertext += self.matrix[(row2 + 1) % 5][col2]
            else:  # Rectangle
                ciphertext += self.matrix[row1][col2]
                ciphertext += self.matrix[row2][col1]
        
        return ciphertext

    def decrypt(self, ciphertext):
        """Decrypt digraphs according to reversed Playfair rules."""
        plaintext = ""
        
        for i in range(0, len(ciphertext), 2):
            row1, col1 = self._find_position(ciphertext[i])
            row2, col2 = self._find_position(ciphertext[i + 1])
            
            if row1 == row2:  # Same row
                plaintext += self.matrix[row1][(col1 - 1) % 5]
                plaintext += self.matrix[row2][(col2 - 1) % 5]
            elif col1 == col2:  # Same column
                plaintext += self.matrix[(row1 - 1) % 5][col1]
                plaintext += self.matrix[(row2 - 1) % 5][col2]
            else:  # Rectangle
                plaintext += self.matrix[row1][col2]
                plaintext += self.matrix[row2][col1]
        
        return plaintext

    @classmethod
    def from_matrix(cls, table_content):
        """Create cipher instance from raw text describing a 5x5 table."""
        # Parse the table - expecting 25 characters (5x5 matrix)
        # Can be formatted as lines or continuous text
        chars = ''.join(c.upper() for c in table_content if c.isalpha())
        
        if len(chars) != 25:
            raise ValueError(f"Table must contain exactly 25 alphabetic characters, got {len(chars)}")
        
        # Create 5x5 matrix
        matrix = []
        for i in range(5):
            matrix.append(list(chars[i*5:(i+1)*5]))
        
        return cls(matrix=matrix)
