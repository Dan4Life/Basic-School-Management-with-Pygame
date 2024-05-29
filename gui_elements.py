import pygame
import time

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

class Button:
    def __init__(self, x, y, width, height, text, font, bg_color, hover_color, text_color, action=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.action = action

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(surface, self.hover_color, self.rect)
        else:
            pygame.draw.rect(surface, self.bg_color, self.rect)

        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos) and self.action:
                self.action()
    
    def collides(self, pos):
        return self.rect.collidepoint(pos)

class InputBox:
    def __init__(self, x, y, width, height, font, text_color, bg_color, active_color, label_text=''):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font
        self.text_color = text_color
        self.bg_color = bg_color
        self.active_color = active_color
        self.text = ''
        self.label_text = label_text
        self.active = False
        self.cursor_visible = True
        self.cursor_timer = time.time()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the input box is clicked, set it to active
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
                self.cursor_visible = True  # Show cursor when box is clicked
                self.cursor_timer = time.time()  # Reset cursor timer
            else:
                self.active = False
        elif event.type == pygame.KEYDOWN:
            # If the input box is active and a key is pressed, add the corresponding character to the text
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    # Handle backspace key repeat
                    self.text = self.text[:-1]
                elif event.key == pygame.K_RETURN:
                    # Optionally, handle pressing enter (e.g., submit form)
                    pass
                else:
                    # Handle other keys being held down for repeated input
                    self.text += event.unicode
                self.cursor_visible = True  # Show cursor when typing
                self.cursor_timer = time.time()  # Reset cursor timer

    def update(self):
        # Ensure the input box is not too long
        if len(self.text) > 30:
            self.text = self.text[:30]

        # Blink the cursor every half second
        if time.time() - self.cursor_timer > 0.5:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = time.time()

    def draw(self, surface):
        # Draw the input box and its text
        color = self.active_color if self.active else self.bg_color
        pygame.draw.rect(surface, color, self.rect)

        # Render label text
        label_surface = self.font.render(self.label_text, True, self.text_color)
        surface.blit(label_surface, (self.rect.x - label_surface.get_width() - 5, self.rect.y + (self.rect.height - label_surface.get_height()) // 2))

        text_surface = self.font.render(self.text, True, self.text_color)
        surface.blit(text_surface, (self.rect.x + 5, self.rect.y + 7))

        # Draw the blinking cursor if the input box is active and visible
        if self.active and self.cursor_visible:
            cursor_x = self.rect.x + 5 + text_surface.get_width()
            pygame.draw.line(surface, self.text_color, (cursor_x, self.rect.y + 8), (cursor_x, self.rect.y + 28))

class Dropdown:
    def __init__(self, x, y, width, height, font, text_color, bg_color, active_color, options, on_select=None, label_text=''):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font
        self.text_color = text_color
        self.bg_color = bg_color
        self.active_color = active_color
        self.options = options
        self.filtered_options = options
        self.current_text = 'Select an option'
        self.expanded = False
        self.active = False
        self.label_text = label_text
        self.label_rect = pygame.Rect(x - 200, y, 200, height)
        self.scroll_offset = 0
        self.max_visible_options = 3
        self.scroll_dragging = False
        self.on_select = on_select  # Callback function for selection

    def handle_event(self, event):
        if event.type == pygame.MOUSEWHEEL and self.expanded:
            self.scroll_offset -= event.y
            self.scroll_offset = max(0, min(self.scroll_offset, len(self.filtered_options) - self.max_visible_options))

        if event.type == pygame.MOUSEBUTTONUP:
            self.scroll_dragging = False

        if event.type == pygame.MOUSEMOTION and self.scroll_dragging:
            new_y = min(max(event.pos[1], self.rect.y + self.rect.height), self.rect.y + self.rect.height + self.rect.height * self.max_visible_options - self.scrollbar_rect.height)
            self.scrollbar_rect.y = new_y
            total_scroll_range = len(self.filtered_options) - self.max_visible_options
            if total_scroll_range > 0:
                self.scroll_offset = int((new_y - (self.rect.y + self.rect.height)) / (self.rect.height * self.max_visible_options - self.scrollbar_rect.height) * total_scroll_range)
            else:
                self.scroll_offset = 0

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.expanded and self.scrollbar_rect:
                if self.scrollbar_rect.collidepoint(event.pos):
                    self.scroll_dragging = True

            if not self.scroll_dragging:
                if self.rect.collidepoint(event.pos):
                    self.current_text = ''
                    self.active = not self.active
                    if not self.active:
                        self.expanded = False
                    else:
                        self.expanded = True
                elif self.expanded:
                    for i, option_rect in enumerate(self.option_rects):
                        if option_rect.collidepoint(event.pos):
                            self.current_text = self.filtered_options[i + self.scroll_offset]
                            self.expanded = False
                            self.active = False
                            if self.on_select:
                                self.on_select(self.current_text)  # Call the callback function
                            break
                    self.active = False
                    self.expanded = False

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.expanded = False
                elif event.key == pygame.K_BACKSPACE:
                    self.current_text = self.current_text[:-1]
                else:
                    self.current_text += event.unicode
                self.filter_options()

    def filter_options(self):
        self.filtered_options = [option for option in self.options if option.lower().startswith(self.current_text.lower())]
        self.scroll_offset = 0

    def update(self):
        self.option_rects = []
        visible_options = self.filtered_options[self.scroll_offset:self.scroll_offset + self.max_visible_options]
        for i, option in enumerate(visible_options):
            option_rect = pygame.Rect(self.rect.x, self.rect.y + self.rect.height * (i + 1), self.rect.width, self.rect.height)
            self.option_rects.append(option_rect)

        total_options_height = len(self.filtered_options) * self.rect.height
        visible_height = self.rect.height * self.max_visible_options
        if total_options_height > visible_height:
            self.scrollbar_height = visible_height / total_options_height * visible_height
        else:
            self.scrollbar_height = visible_height

        if len(self.filtered_options) > self.max_visible_options:
            self.scrollbar_rect = pygame.Rect(
                self.rect.x + self.rect.width - 10,
                self.rect.y + self.rect.height + self.scroll_offset * ((self.rect.height * self.max_visible_options - self.scrollbar_height) / max(1, len(self.filtered_options) - self.max_visible_options)),
                10, self.scrollbar_height
            )
        else:
            self.scrollbar_rect = None

    def draw(self, surface):
        pygame.draw.rect(surface, self.active_color if self.active else self.bg_color, self.rect)
        current_surface = self.font.render(self.current_text, True, self.text_color)
        surface.blit(current_surface, (self.rect.x + 5, self.rect.y + 5))
        self.draw_dropdown_triangle(surface)

        if self.expanded:
            for i, option in enumerate(self.filtered_options[self.scroll_offset:self.scroll_offset + self.max_visible_options]):
                option_rect = self.option_rects[i]
                pygame.draw.rect(surface, self.active_color if option_rect.collidepoint(pygame.mouse.get_pos()) else self.bg_color, option_rect)
                option_surface = self.font.render(option, True, self.text_color)
                surface.blit(option_surface, (option_rect.x + 5, option_rect.y + 5))

            if self.scrollbar_rect:
                pygame.draw.rect(surface, (100, 100, 100), self.scrollbar_rect)

        label_surface = self.font.render(self.label_text, True, self.text_color)
        surface.blit(label_surface, (self.rect.x - label_surface.get_width() - 5, self.rect.y + (self.rect.height - label_surface.get_height()) // 2))

    def draw_dropdown_triangle(self, surface):
        center_x = self.rect.right - 15
        center_y = self.rect.centery
        triangle_size = 10
        points = [
            (center_x, center_y + triangle_size // 2),
            (center_x - triangle_size // 2, center_y - triangle_size // 2),
            (center_x + triangle_size // 2, center_y - triangle_size // 2)
        ]
        pygame.draw.polygon(surface, self.text_color, points)

class Prompt:
    def __init__(self, x, y, width, height, font, duration=2000):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font
        self.text = ""
        self.show_until = 0
        self.duration = duration

    def show(self, text, text_color=pygame.Color('white'), bg_color=pygame.Color('red')):
        self.bg_color = bg_color
        self.text_color = text_color
        self.text = text
        self.show_until = pygame.time.get_ticks() + self.duration

    def update(self):
        if pygame.time.get_ticks() > self.show_until:
            self.text = ""

    def draw(self, surface):
        if self.text:
            pygame.draw.rect(surface, self.bg_color, self.rect)
            rendered_text = self.font.render(self.text, True, self.text_color)
            surface.blit(rendered_text, (self.rect.x + 10, self.rect.y + 10))

class SelectableList:
    def __init__(self, x, y, width, height, font, items, columns):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = font
        self.items = items
        self.columns = columns
        self.selected_items = []

        self.checkbox_size = 20  # Adjust the checkbox size as needed
        self.row_height = 30  # Adjust the row height as needed
        self.scroll_offset = 0
        self.scroll_speed = 20
        self.active = False  # Track if the list is active

        self.dragging = False  # Track if the scrollbar is being dragged
        self.scrollbar_rect = None  # Rect of the scrollbar

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if pygame.Rect(self.x, self.y, self.width, self.height).collidepoint(event.pos):
                self.active = True
                if self.scrollbar_rect and self.scrollbar_rect.collidepoint(event.pos):
                    self.dragging = True
                    self.drag_start_y = event.pos[1]
                    self.scroll_start_offset = self.scroll_offset
            else:
                self.active = False

            if self.active and not self.dragging:
                for checkbox_rect, item, selected, row, column in self.get_visible_checkboxes():
                    if checkbox_rect.collidepoint(event.pos):
                        if selected:
                            self.selected_items.remove(item)
                        else:
                            self.selected_items.append(item)

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:  # Scroll up
            if self.active:
                self.scroll("up")
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:  # Scroll down
            if self.active:
                self.scroll("down")

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False

        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.handle_drag(event)

    def handle_drag(self, event):
        if self.dragging:
            dy = event.pos[1] - self.drag_start_y
            total_items_height = len(self.items) * self.row_height // self.columns
            viewable_ratio = self.height / total_items_height
            new_offset = self.scroll_start_offset + dy / viewable_ratio
            max_scroll_offset = max(0, len(self.items) * self.row_height // self.columns - self.height)
            self.scroll_offset = max(0, min(new_offset, max_scroll_offset))

    def draw(self, screen):
        visible_checkboxes = self.get_visible_checkboxes()
        pygame.draw.rect(screen, (200, 200, 200), (self.x, self.y, self.width, self.height))

        for checkbox_rect, item, selected, row, column in visible_checkboxes:
            # Draw the checkbox
            pygame.draw.rect(screen, (255, 255, 255), checkbox_rect)
            pygame.draw.rect(screen, (0, 0, 0), checkbox_rect, 2)
            if selected:
                pygame.draw.line(screen, (0, 0, 0), checkbox_rect.topleft, checkbox_rect.bottomright, 3)
                pygame.draw.line(screen, (0, 0, 0), checkbox_rect.bottomleft, checkbox_rect.topright, 3)
            
            # Draw the item text
            text_surface = self.font.render(item, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(self.x + (column + 0.5) * self.width / self.columns, self.y + row * self.row_height + self.row_height // 2))
            screen.blit(text_surface, text_rect)

        # Draw the scrollbar
        self.draw_scrollbar(screen)

    def get_visible_checkboxes(self):
        visible_checkboxes = []
        start_index = int(self.scroll_offset // self.row_height)
        end_index = min(len(self.items), int(start_index + self.height // self.row_height))
        for i in range(start_index, end_index):
            row = i - start_index
            for j in range(self.columns):
                item_index = i * self.columns + j
                if item_index < len(self.items):
                    checkbox_rect = pygame.Rect(self.x + j * self.width / self.columns, self.y + row * self.row_height, self.checkbox_size, self.checkbox_size)
                    item = self.items[item_index]
                    selected = (item in self.selected_items)
                    visible_checkboxes.append((checkbox_rect, item, selected, row, j))
        return visible_checkboxes

    def draw_scrollbar(self, screen):
        total_items_height = len(self.items) * self.row_height // self.columns
        if total_items_height > self.height:
            scrollbar_height = max(self.height * (self.height / total_items_height), 20)
            scrollbar_y = self.y + (self.scroll_offset / total_items_height) * self.height
            self.scrollbar_rect = pygame.Rect(self.x + self.width - 10, scrollbar_y, 10, scrollbar_height)
            pygame.draw.rect(screen, (100, 100, 100), self.scrollbar_rect)

    def scroll(self, direction):
        if direction == "up":
            self.scroll_offset = max(0, self.scroll_offset - self.scroll_speed)
        elif direction == "down":
            max_scroll_offset = max(0, len(self.items) * self.row_height // self.columns - self.height)
            self.scroll_offset = min(max_scroll_offset, self.scroll_offset + self.scroll_speed)

class ScrollableTable:
    def __init__(self, x, y, data, screen_height, font, text_color=(0, 0, 0), bg_color=(0, 0, 128), active_color=pygame.Color('dodgerblue'), header_color=pygame.Color('dodgerblue'), row_colors=((173, 216, 230), (240, 248, 255))):
        self.x = x
        self.y = y
        self.data = data
        self.screen_height = screen_height
        self.font = font
        self.text_color = text_color
        self.bg_color = bg_color
        self.active_color = active_color
        self.header_color = header_color
        self.row_colors = row_colors
        self.rows = len(data)
        self.columns = len(data[0]) if data else 0

        self.cell_height = 30  # Fixed cell height
        self.column_widths = self.calculate_column_widths()
        self.table_width = sum(self.column_widths)
        
        self.rect = pygame.Rect(self.x, self.y, self.table_width, self.screen_height)

        self.vertical_scroll_offset = 0
        self.scroll_speed = self.cell_height
        self.is_dragging_vertically = False
        self.vertical_scrollbar_rect = None
        self.active = False

        self.update_vertical_scrollbar_position()
        
    def set_position(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, self.table_width, self.screen_height)
        self.update_vertical_scrollbar_position()

    def calculate_column_widths(self):
        column_widths = [0] * self.columns
        for row in self.data:
            for col_index, cell in enumerate(row):
                cell = str(cell)  # Ensure the cell is a string
                cell_width = self.font.size(cell)[0] + 10  # Adding padding
                if cell_width > column_widths[col_index]:
                    column_widths[col_index] = cell_width
        return column_widths

    def set_data(self, data):
        self.data = data
        self.rows = len(data)
        self.columns = len(data[0]) if data else 0
        self.column_widths = self.calculate_column_widths()
        self.table_width = sum(self.column_widths)
        self.rect = pygame.Rect(self.x, self.y, self.table_width, self.screen_height)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.vertical_scrollbar_rect and self.vertical_scrollbar_rect.collidepoint(event.pos):
                self.is_dragging_vertically = True
                self.mouse_y_start = event.pos[1]
                self.scrollbar_y_start = self.vertical_scrollbar_rect.y
            elif self.rect.collidepoint(event.pos):
                self.active = not self.active

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.is_dragging_vertically = False

        elif event.type == pygame.MOUSEMOTION:
            if self.is_dragging_vertically:
                dy = event.pos[1] - self.mouse_y_start
                new_y = self.scrollbar_y_start + dy
                self.update_vertical_scrollbar_position(new_y)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Scroll up
                self.scroll("up")
            elif event.button == 5:  # Scroll down
                self.scroll("down")

    def scroll(self, direction):
        max_scroll_offset = max(0, (self.rows * self.cell_height) - self.screen_height)
        if direction == "up":
            self.vertical_scroll_offset = max(0, self.vertical_scroll_offset - self.scroll_speed)
        elif direction == "down":
            self.vertical_scroll_offset = min(max_scroll_offset, self.vertical_scroll_offset + self.scroll_speed)
        self.update_vertical_scrollbar_position()

    def update_vertical_scrollbar_position(self, new_y=None):
        max_scroll_offset = max(0, (self.rows * self.cell_height) - self.screen_height)
        if max_scroll_offset == 0:
            return

        if new_y is not None:
            scrollbar_max_y = self.screen_height - self.vertical_scrollbar_rect.height
            new_y = max(self.y + self.cell_height, min(new_y, self.y + scrollbar_max_y))
            self.vertical_scroll_offset = ((new_y - self.y - self.cell_height) / (self.screen_height - self.cell_height - self.vertical_scrollbar_rect.height)) * max_scroll_offset

        scrollbar_height = (self.screen_height - self.cell_height) * (self.screen_height / (self.rows * self.cell_height))
        scrollbar_y = self.y + self.cell_height + (self.vertical_scroll_offset / max_scroll_offset) * (self.screen_height - self.cell_height - scrollbar_height)
        self.vertical_scrollbar_rect = pygame.Rect(self.rect.right - 10, scrollbar_y, 10, scrollbar_height)

    def draw(self, screen):
        visible_rows = (self.screen_height - self.cell_height) // self.cell_height
        start_row = int(self.vertical_scroll_offset // self.cell_height)
        end_row = start_row + visible_rows

        # Draw header
        cell_x = self.x
        for col in range(self.columns):
            cell_value = self.data[0][col]
            cell_rect = pygame.Rect(cell_x, self.y, self.column_widths[col], self.cell_height)
            pygame.draw.rect(screen, self.header_color, cell_rect)
            cell_text = self.font.render(str(cell_value), True, (0, 0, 0))
            pygame.draw.rect(screen, (0, 0, 0), cell_rect, 1)
            text_rect = cell_text.get_rect(center=cell_rect.center)
            screen.blit(cell_text, text_rect)
            cell_x += self.column_widths[col]

        # Draw data rows
        for row in range(start_row + 1, min(end_row + 1, self.rows)):
            cell_x = self.x
            for col in range(self.columns):
                cell_value = self.data[row][col]
                cell_rect = pygame.Rect(cell_x, self.y + (row - start_row) * self.cell_height, self.column_widths[col], self.cell_height)
                pygame.draw.rect(screen, self.row_colors[(row - 1) % len(self.row_colors)], cell_rect)
                cell_text = self.font.render(str(cell_value), True, self.text_color)
                pygame.draw.rect(screen, (0, 0, 0), cell_rect, 1)
                text_rect = cell_text.get_rect(center=cell_rect.center)
                screen.blit(cell_text, text_rect)
                cell_x += self.column_widths[col]

        self.draw_scrollbar(screen)

    def draw_scrollbar(self, screen):
        if self.rows * self.cell_height > self.screen_height:
            pygame.draw.rect(screen, self.active_color if self.is_dragging_vertically else (100, 100, 100), self.vertical_scrollbar_rect)
        else:
            self.vertical_scrollbar_rect = None