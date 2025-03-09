def update_board_size(screen, board_size, cell_size):
    width, height = screen.get_size()
    cell_size = min(width / board_size, height / board_size) * 0.9
    offset_x = (width - cell_size * board_size) / 2
    offset_y = (height - cell_size * board_size) / 2
    return cell_size, offset_x, offset_y
