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
        pass

    def _prepare_text(self, text):
        """Normalize and split text into digraphs according to Playfair rules."""
        pass

    def encrypt(self, plaintext):
        """Encrypt digraphs according to Playfair transformation rules."""
        pass

    def decrypt(self, ciphertext):
        """Decrypt digraphs according to reversed Playfair rules."""
        pass

    @classmethod
    def from_matrix(cls, table_content):
        """Create cipher instance from raw text describing a 5×5 table."""
        pass
