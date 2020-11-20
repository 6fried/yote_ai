"""
Created on 19 nov. 09:18 2020

@author: 6fried
"""

from core import Player, Color
from yote.yote_rules import YoteRules
from yote.yote_action import YoteAction, YoteActionType


class AI(Player):
    """Coordinates are like (y, x)"""

    name = "Selecta AI"

    def __init__(self, color):
        super(AI, self).__init__(color)
        self.position = color.value

    def play(self, state, remain_time):
        print("time remain is ", remain_time, " seconds")
        board = state.get_board()
        latest_move = state.get_latest_move()
        latest_player = state.get_latest_player()
        if (
            len(board.get_all_empty_cells())
            == board.board_shape[0] * board.board_shape[1]
        ):
            return YoteAction(
                action_type=YoteActionType.ADD,
                to=(
                    board.board_shape[0] // 2,
                    board.board_shape[1] // 2,
                ),
            )
        if latest_player == self.position:  # state.rewarding_move:
            return self.steal(state)
        return self.provide(state)

    def provide(self, state):
        board = state.get_board()
        empty_cells = board.get_all_empty_cells()
        me = board.get_player_pieces_on_board(Color(self.position))
        opponents = board.get_player_pieces_on_board(Color(-self.position))
        available_moves = YoteRules.get_player_actions(state, self.position)

        def is_dangerous_cell(cell):
            if (
                (cell[0] - 1, cell[1]) in opponents
                and (cell[0] + 1, cell[1]) in empty_cells
                or (cell[0] + 1, cell[1]) in opponents
                and (cell[0] - 1, cell[1]) in empty_cells
                or (cell[0], cell[1] - 1) in opponents
                and (cell[0], cell[1] + 1) in empty_cells
                or (cell[0], cell[1] + 1) in opponents
                and (cell[0], cell[1] - 1) in empty_cells
            ):
                return True
            else:
                return False

        if state.get_latest_player() == self.position:
            return self.steal(state)

        for cell in me:  # Just take the opponents piece
            if (cell[0] - 1, cell[1]) in opponents:
                if (cell[0] - 2, cell[1]) in empty_cells:
                    return YoteAction(
                        action_type=YoteActionType.MOVE,
                        at=cell,
                        to=(cell[0] - 2, cell[1]),
                    )
            if (cell[0] + 1, cell[1]) in opponents:
                if (cell[0] + 2, cell[1]) in empty_cells:
                    return YoteAction(
                        action_type=YoteActionType.MOVE,
                        at=cell,
                        to=(cell[0] + 2, cell[1]),
                    )
            if (cell[0], cell[1] - 1) in opponents:
                if (cell[0], cell[1] - 2) in empty_cells:
                    return YoteAction(
                        action_type=YoteActionType.MOVE,
                        at=cell,
                        to=(cell[0], cell[1] - 2),
                    )
            if (cell[0], cell[1] + 1) in opponents:
                if (cell[0], cell[1] + 2) in empty_cells:
                    return YoteAction(
                        action_type=YoteActionType.MOVE,
                        at=cell,
                        to=(cell[0], cell[1] + 2),
                    )

        for cell in me:  #  just run away
            if (cell[0], cell[1] - 1) in opponents:
                if (
                    (cell[0], cell[1] + 1) in empty_cells
                    and (cell[0], cell[1] + 2) not in opponents
                    and not (
                        (cell[0] - 1, cell[1] + 1) in opponents and cell[0] + 1,
                        cell[1] + 1,
                    )
                    in empty_cells
                    or (cell[0] + 1, cell[1] + 1) in opponents
                    and (cell[0] - 1, cell[1] + 1) in empty_cells
                ):
                    return YoteAction(
                        action_type=YoteActionType.MOVE,
                        at=cell,
                        to=(cell[0], cell[1] + 1),
                    )
            if (cell[0] - 1, cell[1]) in opponents:
                if (
                    (cell[0] + 1, cell[1]) in empty_cells
                    and (cell[0] + 2, cell[1]) not in opponents
                    and not (
                        (cell[0] + 1, cell[1] - 1) in opponents and cell[0] + 1,
                        cell[1] + 1,
                    )
                    in empty_cells
                    or (cell[0] + 1, cell[1] + 1) in opponents
                    and (cell[0] + 1, cell[1] - 1) in empty_cells
                ):
                    return YoteAction(
                        action_type=YoteActionType.MOVE,
                        at=cell,
                        to=(cell[0] + 1, cell[1]),
                    )
            if (cell[0] + 1, cell[1]) in opponents:
                if (
                    (cell[0] - 1, cell[1]) in empty_cells
                    and (cell[0] - 2, cell[1]) not in opponents
                    and not (
                        (cell[0] - 1, cell[1] - 1) in opponents and cell[0] - 1,
                        cell[1] + 1,
                    )
                    in empty_cells
                    or (cell[0] - 1, cell[1] + 1) in opponents
                    and (cell[0] - 1, cell[1] - 1) in empty_cells
                ):
                    return YoteAction(
                        action_type=YoteActionType.MOVE,
                        at=cell,
                        to=(cell[0] - 1, cell[1]),
                    )
            if (cell[0], cell[1] + 1) in opponents:
                if (
                    (cell[0], cell[1] - 1) in empty_cells
                    and (cell[0], cell[1] - 2) not in opponents
                    and not (
                        (cell[0] - 1, cell[1] - 1) in opponents and cell[0] + 1,
                        cell[1] - 1,
                    )
                    in empty_cells
                    or (cell[0] + 1, cell[1] - 1) in opponents
                    and (cell[0] - 1, cell[1] - 1) in empty_cells
                ):
                    return YoteAction(
                        action_type=YoteActionType.MOVE,
                        at=cell,
                        to=(cell[0], cell[1] - 1),
                    )

        for cell in me:
            if (cell[0], cell[1] - 1) in empty_cells and (
                cell[0],
                cell[1] - 2,
            ) not in opponents:
                if (
                    (cell[0] + 1, cell[1] - 1) in opponents
                    and (cell[0] - 1, cell[1] - 1) not in empty_cells
                    or (cell[0] - 1, cell[1] - 1) in opponents
                    and (cell[0] + 1, cell[1] - 1) not in empty_cells
                ):
                    return YoteAction(
                        action_type=YoteActionType.MOVE,
                        at=cell,
                        to=(cell[0], cell[1] - 1),
                    )
            if (cell[0], cell[1] + 1) in empty_cells and (
                cell[0],
                cell[1] + 2,
            ) not in opponents:
                if (
                    (cell[0] + 1, cell[1] + 1) in opponents
                    and (cell[0] - 1, cell[1] + 1) not in opponents
                    or (cell[0] - 1, cell[1] + 1) in opponents
                    and (cell[0] + 1, cell[1] + 1) not in opponents
                ):
                    return YoteAction(
                        action_type=YoteActionType.MOVE,
                        at=cell,
                        to=(cell[0], cell[1] + 1),
                    )
            if (cell[0] - 1, cell[1]) in empty_cells and (
                cell[0] - 2,
                cell[1],
            ) not in opponents:
                if (
                    (cell[0] - 1, cell[1] - 1) in opponents
                    and (cell[0] - 1, cell[1] - 1) not in opponents
                    or (cell[0] - 1, cell[1] + 1) in opponents
                    and (cell[0] - 1, cell[1] - 1) not in opponents
                ):
                    return YoteAction(
                        action_type=YoteActionType.MOVE,
                        at=cell,
                        to=(cell[0] - 1, cell[1]),
                    )
            if (cell[0] + 1, cell[1]) in empty_cells and (
                cell[0] + 2,
                cell[1],
            ) not in opponents:
                if (
                    (cell[0] + 1, cell[1] - 1) in opponents
                    and (cell[0] + 1, cell[1] + 1) not in opponents
                    or (cell[0] + 1, cell[1] + 1) in opponents
                    and (cell[0] + 1, cell[1] - 1) not in opponents
                ):
                    return YoteAction(
                        action_type=YoteActionType.MOVE,
                        at=cell,
                        to=(cell[0] + 1, cell[1]),
                    )

        for cell in me:
            if (cell[0], cell[1] - 1) in empty_cells and (
                cell[0],
                cell[1] - 2,
            ) not in opponents:
                if (
                    (cell[0], cell[1] - 3) in opponents
                    and (cell[0], cell[1] - 2) not in opponents
                    or (cell[0] + 2, cell[1] - 1) in opponents
                    and (cell[0] + 1, cell[1] - 1) not in opponents
                    or (cell[0] - 2, cell[1] - 1) in opponents
                    and (cell[0] - 1, cell[1] - 1) not in opponents
                ):
                    return YoteAction(
                        action_type=YoteActionType.MOVE,
                        at=cell,
                        to=(cell[0], cell[1] - 1),
                    )
            if (cell[0], cell[1] + 1) in empty_cells and (
                cell[0],
                cell[1] + 2,
            ) not in opponents:
                if (
                    (cell[0], cell[1] + 3) in opponents
                    and (cell[0], cell[1] + 2) not in opponents
                    or (cell[0] + 2, cell[1] + 1) in opponents
                    and (cell[0] + 1, cell[1] + 1) not in opponents
                    or (cell[0] - 2, cell[1] + 1) in opponents
                    and (cell[0] - 1, cell[1] + 1) not in opponents
                ):
                    return YoteAction(
                        action_type=YoteActionType.MOVE,
                        at=cell,
                        to=(cell[0], cell[1] + 1),
                    )
            if (cell[0] - 1, cell[1]) in empty_cells and (
                cell[0] - 2,
                cell[1],
            ) not in opponents:
                if (
                    (cell[0] - 3, cell[1]) in opponents
                    and (cell[0] - 2, cell[1]) not in opponents
                    or (cell[0] - 1, cell[1] - 2) in opponents
                    and (cell[0] - 1, cell[1] - 1) not in opponents
                    or (cell[0] - 1, cell[1] + 2) in opponents
                    and (cell[0] - 1, cell[1] + 1) not in opponents
                ):
                    return YoteAction(
                        action_type=YoteActionType.MOVE,
                        at=cell,
                        to=(cell[0] - 1, cell[1]),
                    )
            if (cell[0] + 1, cell[1]) in empty_cells and (
                cell[0] + 2,
                cell[1],
            ) not in opponents:
                if (
                    (cell[0] + 3, cell[1]) in opponents
                    and (cell[0] + 2, cell[1]) not in opponents
                    or (cell[0] + 1, cell[1] - 2) in opponents
                    and (cell[0] + 1, cell[1] - 1) not in opponents
                    or (cell[0] + 1, cell[1] + 2) in opponents
                    and (cell[0] + 1, cell[1] + 1) not in opponents
                ):
                    return YoteAction(
                        action_type=YoteActionType.MOVE,
                        at=cell,
                        to=(cell[0] + 1, cell[1]),
                    )

        if state.get_player_info(self.position)["in_hand"] > 0:
            return self.add(board)
        else:
            return available_moves[0]

    def steal(self, state):
        board = state.get_board()
        empty_cells = board.get_all_empty_cells()
        me = board.get_player_pieces_on_board(Color(self.position))
        opponents = board.get_player_pieces_on_board(Color(-self.position))
        latest_move = state.get_latest_move()
        prior_cell = latest_move["action"]["to"]

        if len(opponents) > 0:
            # Protect just moved piece
            if (prior_cell[0] - 1, prior_cell[1]) in opponents:
                if (prior_cell[0] + 1, prior_cell[1]) in empty_cells:
                    return YoteAction(
                        action_type=YoteActionType.STEAL_FROM_BOARD,
                        at=(prior_cell[0] - 1, prior_cell[1]),
                    )
            if (prior_cell[0] + 1, prior_cell[1]) in opponents:
                if (prior_cell[0] - 1, prior_cell[1]) in empty_cells:
                    return YoteAction(
                        action_type=YoteActionType.STEAL_FROM_BOARD,
                        at=(prior_cell[0] + 1, prior_cell[1]),
                    )
            if (prior_cell[0], prior_cell[1] - 1) in opponents:
                if (prior_cell[0], prior_cell[1] + 1) in empty_cells:
                    return YoteAction(
                        action_type=YoteActionType.STEAL_FROM_BOARD,
                        at=(prior_cell[0], prior_cell[1] - 1),
                    )
            if (prior_cell[0], prior_cell[1] + 1) in opponents:
                if (prior_cell[0], prior_cell[1] - 1) in empty_cells:
                    return YoteAction(
                        action_type=YoteActionType.STEAL_FROM_BOARD,
                        at=(prior_cell[0], prior_cell[1] + 1),
                    )

            for cell in opponents:  # Protect the other pieces
                if (
                    (
                        (cell[0] - 1, cell[1]) in me
                        and (cell[0] - 2, cell[1]) in empty_cells
                    )
                    or (
                        (cell[0] + 1, cell[1]) in me
                        and (cell[0] + 2, cell[1]) in empty_cells
                    )
                    or (
                        (cell[0], cell[1] - 1) in me
                        and (cell[0], cell[1] - 2) in empty_cells
                    )
                    or (
                        (cell[0], cell[1] + 1) in me
                        and (cell[0], cell[1] + 2) in empty_cells
                    )
                ):
                    return YoteAction(
                        action_type=YoteActionType.STEAL_FROM_BOARD, at=cell
                    )
            return YoteAction(
                action_type=YoteActionType.STEAL_FROM_BOARD, at=opponents[0]
            )

        else:
            return YoteAction(action_type=YoteActionType.STEAL_FROM_HAND)

    def add(self, board):
        empty_cells = board.get_all_empty_cells()
        me = board.get_player_pieces_on_board(Color(self.position))
        opponents = board.get_player_pieces_on_board(Color(-self.position))

        for cell in opponents:  # on board_imit
            if cell[1] - 1 == 0 and (cell[0], cell[1] - 1) in empty_cells:
                return YoteAction(
                    action_type=YoteActionType.ADD, to=(cell[0], cell[1] - 1)
                )
            elif cell[0] - 1 == 0 and (cell[0] - 1, cell[1]) in empty_cells:
                return YoteAction(
                    action_type=YoteActionType.ADD, to=(cell[0] - 1, cell[1])
                )
            elif (
                cell[0] + 1 == board.board_shape[0]
                and (cell[0] + 1, cell[1]) in empty_cells
            ):
                return YoteAction(
                    action_type=YoteActionType.ADD, to=(cell[0] + 1, cell[1])
                )
            elif (
                cell[1] + 1 == board.board_shape[1]
                and (cell[0], cell[1] + 1) in empty_cells
            ):
                return YoteAction(
                    action_type=YoteActionType.ADD, to=(cell[0], cell[1] + 1)
                )

        for cell in opponents:  # consecutives
            if (cell[0], cell[1] - 2) in me and (cell[0], cell[1] - 1) in empty_cells:
                return YoteAction(
                    action_type=YoteActionType.ADD, to=(cell[0], cell[1] - 1)
                )
            if (cell[0] - 2, cell[1]) in me and (cell[0] - 1, cell[1]) in empty_cells:
                return YoteAction(
                    action_type=YoteActionType.ADD, to=(cell[0] - 1, cell[1])
                )
            if (cell[0] + 2, cell[1]) in me and (cell[0] + 1, cell[1]) in empty_cells:
                return YoteAction(
                    action_type=YoteActionType.ADD, to=(cell[0] + 1, cell[1])
                )
            if (cell[0], cell[1] + 2) in me and (cell[0], cell[1] + 1) in empty_cells:
                return YoteAction(
                    action_type=YoteActionType.ADD, to=(cell[0], cell[1] + 1)
                )

        for cell in opponents:  # block
            if (
                (cell[0], cell[1] - 2) in empty_cells
                and (cell[0], cell[1] - 1) in empty_cells
                and not ((cell[0], cell[1] - 3) in opponents)
            ):
                if (cell[0], cell[1] - 2) in empty_cells:
                    return YoteAction(
                        action_type=YoteActionType.ADD, to=(cell[0], cell[1] - 2)
                    )
            if (
                (cell[0] - 2, cell[1]) in empty_cells
                and (cell[0] - 1, cell[1]) in empty_cells
                and not ((cell[0] - 3, cell[1]) not in opponents)
            ):
                if (cell[0] - 2, cell[1]) in empty_cells:
                    return YoteAction(
                        action_type=YoteActionType.ADD, to=(cell[0] - 2, cell[1])
                    )
            if (
                (cell[0] + 2, cell[1]) in empty_cells
                and (cell[0] + 1, cell[1]) in empty_cells
                and not ((cell[0] + 3, cell[1]) not in opponents)
            ):
                if (cell[0] + 2, cell[1]) in empty_cells:
                    return YoteAction(
                        action_type=YoteActionType.ADD, to=(cell[0] + 2, cell[1])
                    )
            if (
                (cell[0], cell[1] + 2) in empty_cells
                and (cell[0], cell[1] + 1) in empty_cells
                and not ((cell[0], cell[1] + 3) not in opponents)
            ):
                if (cell[0], cell[1] + 2) in empty_cells:
                    return YoteAction(
                        action_type=YoteActionType.ADD, to=(cell[0], cell[1] + 2)
                    )

        return YoteAction(action_type=YoteActionType.ADD, to=empty_cells[0])
