import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if self.count == len(self.cells):
            return self.cells
        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        return set()
    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        self.moves_made.add(cell)

        self.mark_safe(cell)
        
        #Creates new sentence with all cells and marks the given cell as safe
        new_sentence = Sentence({}, count)
        for i in range(-1, 2):
            for j in range(-1, 2):
                if cell[0] + i in range(0, self.height) and cell[1] + j in range(0, self.width):
                    new_sentence.cells.add((cell[0] + i, cell[1] + j))
        new_sentence.cells.remove(cell)
        #Reduces the new sentence given the knowledge
        temp_set = new_sentence.cells.copy()
        for is_known_cell in temp_set:
            if is_known_cell in self.safes:
                new_sentence.mark_safe(is_known_cell) 
            if is_known_cell in self.mines:
                new_sentence.mark_mine(is_known_cell)
        
        if new_sentence.cells == {}:
            return #If empty set it provides no info and cannot be reduced
        
        #Adds the new sentence to the knowledge
        self.knowledge.append(new_sentence)
        #generates new sentences given the new one
        temp_set = []
        for sentence in self.knowledge:
            inference_sentence = Sentence({}, 0)
            if sentence.cells <= new_sentence.cells:
                inference_sentence.count = new_sentence.count - sentence.count
                inference_sentence.cells = new_sentence.cells.copy()
                for known_cell in sentence.cells:
                    inference_sentence.cells.remove(known_cell)
                temp_set.append(inference_sentence)
        for item in temp_set:
            self.knowledge.append(item)

        temp_knowledge1 = self.knowledge.copy()
        for choice_sentence in temp_knowledge1:
            temp_set = choice_sentence.cells.copy()
            if choice_sentence.count == len(choice_sentence.cells):
                for mine in temp_set:
                    self.mark_mine(mine)
            elif choice_sentence.count == 0:
                for safe in temp_set:
                    self.mark_safe(safe)

            temp_knowledge2 = self.knowledge.copy()
            for sentence in temp_knowledge2:
                inference_sentence = Sentence({}, 0)
                if sentence.cells <= choice_sentence.cells:
                    inference_sentence.count = choice_sentence.count - sentence.count
                    inference_sentence.cells = choice_sentence.cells.copy()
                    for known_cell in sentence.cells:
                        inference_sentence.cells.remove(known_cell)
                    self.knowledge.append(inference_sentence)
            
        #for sentence in self.knowledge:
        #    if sentence.count == len(sentence.cells):
        #        for mine in sentence.cells:
        #            self.mark_mine(mine)
        #    elif sentence.count == 0:
        #        for safe in sentence.cells:
        #            self.mark_safe(safe)
        
        #Updates knowledge given the new sentence / new inferences
        #Check for sentences with count=len or count=0
        for i in range(len(self.knowledge) - 1):
            print(self.knowledge)
            print(i)
            try:    
                if self.knowledge[i].count == 0 or self.knowledge[i].count == len(self.knowledge[i].cells):
                    self.knowledge.pop(i)
            except IndexError:
                pass
    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for move in self.safes:
            if move not in self.moves_made:
                return move
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        if len(self.mines) + len(self.moves_made) == self.width * self.height:
                return None
        
        while True:    
            random_move = (random.randint(0, self.width - 1), random.randint(0, self.height - 1))
            if random_move not in self.mines and random_move not in self.moves_made:
                return random_move
