# Veidojis Dāvis Lektauers, 10.1
# Darbs sākts 2023. g. 24. aprīlī

import math, re

import renderer as r
import common
import parser

def start():
    pass
r.on_start(start)

def find_error_cols(table, column):
    if len(common.table_data[table]["content"][column]["content"][1]["value"].strip()) > 0 and \
        common.table_data[table]["content"][column]["content"][1]["value"].strip()[0] != "=":

        return [("num", column)]

    error_cols = []
    tokens = parser.str_to_tokens(common.table_data[table]["content"][column]["content"][1]["value"][1:])

    for t in tokens:
        if t.type == parser.TokenType.IDENTIFIER:
            identifier = parser.parse_identifier(t)
            col = common.ALPHABET.index(identifier[1])
            error_cols = error_cols + [("intermediary", column)] + find_error_cols(identifier[0], col)
    
    return list(dict.fromkeys(error_cols)) # Removes duplicates from error_cols (https://www.w3schools.com/python/python_howto_remove_duplicates.asp)

scroll_y = 0
table_scroll_x = {}
table_areas = {}
text_cursor_pos = 0
selected_cell = None
def update(info):
    global scroll_y, table_scroll_x, table_areas, text_cursor_pos, selected_cell

    r.render_rect((0, 0, r.width, r.height), (255, 255, 255))

    ## TABLE RENDERING ##
    curr_table_y = 0
    for i in common.table_data:
        curr_table_y += 20

        if table_scroll_x.get(i) == None:
            table_scroll_x[i] = 0

        x_offset = -table_scroll_x[i]
        y_offset = curr_table_y - scroll_y

        r.render_text(f"{i}. tabula", (x_offset + 10, y_offset), 24)
        y_offset += 30
        
        curr_cell_x = 0
        curr_cell_y = 0

        for col in range(common.table_data[i]["width"] + 1):
            curr_cell_y = 0

            for row in range(common.table_data[i]["height"] + 2):
                cell_width = 200
                cell_height = 30

                if col == 0 and row == 0:
                    # Corner cell
                    cell_width = 25
                    cell_height = 25
                elif col == 0:
                    # Column letters
                    cell_width = 15

                    if row > 1:
                        r.render_text(str(row-1), (x_offset + curr_cell_x + 1, y_offset + curr_cell_y), 12, (50, 50, 50))
                elif row == 0:
                    # Row numbers
                    cell_height = 15

                    r.render_text(common.ALPHABET[col-1], (x_offset + curr_cell_x + 2, y_offset + curr_cell_y), 12, (50, 50, 50))
                else:
                    # Regular cells
                    cell = common.table_data[i]["content"][col-1]["content"][row-1]
                    
                    is_selected = selected_cell != None and selected_cell[0] == i and selected_cell[1] == col and selected_cell[2] == row
                    
                    cell_text = cell["value"]
                    if is_selected:
                        cell_text = cell_text[:text_cursor_pos] + "|" + cell_text[text_cursor_pos:]
                    else:
                        cell_text = cell["parsed_value"]
                    
                    if cell["has_error"]:
                        text_color = (232, 58, 58)
                    elif row == 1:
                        text_color = (50, 50, 50)
                    else:
                        text_color = (0, 0, 0)
                     
                    if row == 1:
                        # Table header
                        if common.table_data[i]["content"][col-1]["error_col"]:
                            r.render_rect((x_offset + curr_cell_x, y_offset + curr_cell_y, cell_width, cell_height), (160, 160, 160))
                        else:
                            r.render_rect((x_offset + curr_cell_x, y_offset + curr_cell_y, cell_width, cell_height), (200, 200, 200))
                        
                        r.render_hrect((x_offset + curr_cell_x, y_offset + curr_cell_y, cell_width, cell_height), (50, 50, 50))

                        r.render_text(
                            cell_text,
                            (x_offset + curr_cell_x + 5, y_offset + curr_cell_y + 6), 16, text_color
                        )
                    else:
                        # Table cells
                        r.render_hrect((x_offset + curr_cell_x, y_offset + curr_cell_y, cell_width, cell_height))

                        r.render_text(
                            cell_text, 
                            (x_offset + curr_cell_x + 5, y_offset + curr_cell_y + 6), 16, text_color
                        )
                    
                    if is_selected:
                        r.render_hrect((x_offset + curr_cell_x, y_offset + curr_cell_y, cell_width, cell_height), (244, 127, 17))
                    
                    if not is_selected and r.is_mouse_down and r.mouse_pos[0] > x_offset + curr_cell_x and r.mouse_pos[1] > y_offset + curr_cell_y and \
                        r.mouse_pos[0] < x_offset + curr_cell_x + cell_width and r.mouse_pos[1] < y_offset + curr_cell_y + cell_height:

                        selected_cell = (i, col, row)
                        text_cursor_pos = len(cell["value"])
                
                # Adding new cols
                if row > 0 and col > 0:
                    if abs(x_offset + curr_cell_x + cell_width - r.mouse_pos[0]) < 5 and \
                        r.mouse_pos[1] > y_offset + curr_cell_y and r.mouse_pos[1] < y_offset + curr_cell_y + cell_height:

                        r.render_rect((x_offset + curr_cell_x + cell_width - 5, y_offset + curr_cell_y, 10, cell_height), (244, 127, 17))

                        if r.is_mouse_just_down and common.table_data[i]["width"] < len(common.ALPHABET):
                            common.table_data[i]["content"] = common.table_data[i]["content"][:col] + [{"content": [], "error_col": False}] + common.table_data[i]["content"][col:]

                            for rc in range(common.table_data[i]["height"]+1):
                                common.table_data[i]["content"][col]["content"].append({"value": "", "parsed_value": "", "has_error": False})

                            common.table_data[i]["width"] += 1

                            r.is_mouse_just_down = False

                            selected_cell = None

                # Adding new rows
                if row > 0 and col > 0:
                    if abs(y_offset + curr_cell_y + cell_height - r.mouse_pos[1]) < 5 and \
                        r.mouse_pos[0] > x_offset + curr_cell_x and r.mouse_pos[0] < x_offset + curr_cell_x + cell_width:

                        r.render_rect((x_offset + curr_cell_x, y_offset + curr_cell_y + cell_height - 5, cell_width, 10), (244, 127, 17))

                        if r.is_mouse_just_down:
                            for tc in common.table_data[i]["content"]:
                                tc["content"] = tc["content"][:row] + [{"value": "", "parsed_value": "", "has_error": False}] + tc["content"][row:]

                            common.table_data[i]["height"] += 1

                            selected_cell = None
                
                # Autofill
                if row > 3 and r.is_mouse_right_just_down and common.table_data[i]["content"][col-1]["content"][row-1]["value"].strip() == "" and \
                    r.mouse_pos[0] > x_offset + curr_cell_x and r.mouse_pos[1] > y_offset + curr_cell_y and \
                    r.mouse_pos[0] < x_offset + curr_cell_x + cell_width and r.mouse_pos[1] < y_offset + curr_cell_y + cell_height:

                    second_last_value = common.table_data[i]["content"][col-1]["content"][row-3]["value"]
                    last_value = common.table_data[i]["content"][col-1]["content"][row-2]["value"]

                    if last_value != None and second_last_value != None:
                        if len(last_value.strip()) > 0 and last_value.strip()[0] == "=" and \
                            len(second_last_value.strip()) > 0 and second_last_value.strip()[0] == "=":
                            
                            curr_tc = row - 1
                            prev_expr = last_value[1:]
                            while True:
                                try:
                                    incremented_expr = parser.increment_expression(prev_expr)
                                except:
                                    break

                                common.table_data[i]["content"][col-1]["content"][curr_tc]["value"] = "=" + incremented_expr

                                try:
                                    common.table_data[i]["content"][col-1]["content"][curr_tc]["parsed_value"] = str(parser.parse(incremented_expr))
                                except:
                                    common.table_data[i]["content"][col-1]["content"][curr_tc]["parsed_value"] = "#ERR"
                                    common.table_data[i]["content"][col-1]["content"][curr_tc]["has_error"] = True

                                curr_tc += 1
                                if curr_tc > common.table_data[i]["height"] or \
                                    common.table_data[i]["content"][col-1]["content"][curr_tc]["value"].strip() != "":
                                    
                                    break
                                
                                prev_expr = common.table_data[i]["content"][col-1]["content"][curr_tc-1]["value"][1:]

                        elif re.match(r"[0-9]|\.", last_value) and re.match(r"[0-9]|\.", second_last_value):
                            diff = float(last_value) - float(second_last_value)

                            curr_tc = row - 1
                            curr_val = float(last_value)
                            while True:
                                curr_val += diff

                                display_value = str(curr_val)
                                if math.floor(curr_val) == curr_val and math.floor(diff) == diff:
                                    display_value = str(int(curr_val))
                                
                                common.table_data[i]["content"][col-1]["content"][curr_tc]["value"] = display_value
                                common.table_data[i]["content"][col-1]["content"][curr_tc]["parsed_value"] = display_value

                                curr_tc += 1
                                if curr_tc > common.table_data[i]["height"] or \
                                    common.table_data[i]["content"][col-1]["content"][curr_tc]["value"].strip() != "":
                                    
                                    break
                    
                curr_cell_y += cell_height

            curr_cell_x += cell_width
        
        table_areas[i] = (curr_table_y, curr_table_y + curr_cell_y + 30)
        
        curr_table_y += curr_cell_y + 50
    
    ## NEW TABLE BUTTON ##
    curr_table_y += 20
    new_table_btn_boundaries = (10, curr_table_y - scroll_y, 400, 50)
    r.render_rect((10, curr_table_y - scroll_y, 400, 50), (200, 200, 200))
    r.render_text("+ Pievienot tabulu", (new_table_btn_boundaries[0] + 70, new_table_btn_boundaries[1] + 8), 30, (50, 50, 50))

    if r.is_mouse_down and r.mouse_pos[0] > new_table_btn_boundaries[0] and r.mouse_pos[1] > new_table_btn_boundaries[1] and \
        r.mouse_pos[0] < new_table_btn_boundaries[0] + new_table_btn_boundaries[2] and r.mouse_pos[1] < new_table_btn_boundaries[1] + new_table_btn_boundaries[3]:

        common.table_data[len(common.table_data) + 1] = {
            "width": 1,
            "height": 1,
            "content": [{
                "error_col": False,
                "content": [{"value": "", "parsed_value": "", "has_error": False}, {"value": "", "parsed_value": "", "has_error": False}]
            }]
        }
    
    ## SCROLLING ##
    if r.mouse_scroll != 0:
        scroll_diff = 0
        if r.mouse_scroll > 0:
            scroll_diff = -50
        elif r.mouse_scroll < 0:
            scroll_diff = 50
        
        scrolled_table = False
        for a in table_areas:
            if "[SHIFT]" in r.pressed_keys and r.mouse_pos[1] > table_areas[a][0] - scroll_y and r.mouse_pos[1] < table_areas[a][1] - scroll_y:
                table_scroll_x[a] += scroll_diff
                scrolled_table = True

                if table_scroll_x[a] < 0:
                    table_scroll_x[a] = 0
                    scrolled_table = False
        
        if not scrolled_table:
            scroll_y += scroll_diff

            if scroll_y < 0:
                scroll_y = 0
    
    ## TEXT INPUT ##
    if selected_cell != None and len(r.just_pressed_keys) > 0:
        cell_pos = selected_cell
        cell = common.table_data[cell_pos[0]]["content"][cell_pos[1]-1]["content"][cell_pos[2]-1]
        new_char = r.just_pressed_keys[0]

        if new_char == "[ARR_LEFT]":
            text_cursor_pos -= 1
            if text_cursor_pos < 0:
                text_cursor_pos = 0

        elif new_char == "[ARR_RIGHT]":
            text_cursor_pos += 1
            if text_cursor_pos > len(cell["value"]):
                text_cursor_pos = len(cell["value"])

        elif new_char == "[ARR_UP]":
            if selected_cell[2] >= 0:
                selected_cell = (selected_cell[0], selected_cell[1], selected_cell[2]-1)

        elif new_char == "[ARR_DOWN]" or new_char == "[RETURN]":
            if selected_cell[2] <= common.table_data[selected_cell[0]]["height"]:
                selected_cell = (selected_cell[0], selected_cell[1], selected_cell[2]+1)
            else:
                selected_cell = None

        elif new_char == "[BACKSPACE]":
            if text_cursor_pos > 0:
                cell["value"] = cell["value"][:text_cursor_pos-1] + cell["value"][text_cursor_pos:]
                text_cursor_pos -= 1

        elif new_char == "[DELETE]":
            if text_cursor_pos < len(cell["value"]):
                cell["value"] = cell["value"][:text_cursor_pos] + cell["value"][text_cursor_pos+1:]

        elif not (len(new_char) > 1 and new_char[0] == "[") and new_char != "":
            cell["value"] = cell["value"][:text_cursor_pos] + new_char + cell["value"][text_cursor_pos:]
            text_cursor_pos += 1

        elif new_char == "[ESC]":
            selected_cell = None

        elif new_char == "[TAB]":
            ## ERROR CALCULATION ##
            ecols = find_error_cols(selected_cell[0], selected_cell[1]-1)

            while len(ecols) > 0:
                if ecols[0][1] != selected_cell[1]:
                    table = common.table_data[selected_cell[0]]["content"]
                    common.table_data[selected_cell[0]]["content"] = table[:ecols[0][1]+1] + [{"error_col": True, "content": []}] + table[ecols[0][1]+1:]

                    for i in range(common.table_data[selected_cell[0]]["height"]+1):
                        if i == 0:
                            header_value = common.table_data[selected_cell[0]]["content"][ecols[0][1]]["content"][0]["value"]
                            err_header_value = f"&cdelta;{header_value}"

                            common.table_data[selected_cell[0]]["content"][ecols[0][1]+1]["content"].append({
                                "value": err_header_value,
                                "parsed_value": parser.parse_text(err_header_value),
                                "has_error": False
                            })
                        else:
                            common.table_data[selected_cell[0]]["content"][ecols[0][1]+1]["content"].append({
                                "value": "=0",
                                "parsed_value": str(parser.parse("0")),
                                "has_error": False
                            })
                    common.table_data[selected_cell[0]]["width"] += 1
                
                for i in range(len(ecols)):
                    if ecols[i][1] > ecols[0][1]:
                        ecols[i] = (ecols[i][0], ecols[i][1] + 1)

                ecols.pop(0)

        if len(cell["value"].strip()) > 0 and cell["value"].strip()[0] == "=":
            # Parse expressions
            try:
                parsed_exp = parser.parse(cell["value"].strip()[1:])

                parsed_value = str(parsed_exp)
                if math.floor(parsed_exp) == parsed_exp:
                    parsed_value = str(int(parsed_exp))

                cell["parsed_value"] = parsed_value
                cell["has_error"] = False
            except:
                cell["parsed_value"] = "#ERR"
                cell["has_error"] = True
        else:
            # Parse text cells
            cell["parsed_value"] = parser.parse_text(cell["value"])

        common.table_data[cell_pos[0]]["content"][cell_pos[1]-1]["content"][cell_pos[2]-1] = cell
    
    ## SHORTCUTS ##
    if "[F12]" in r.just_pressed_keys:
        common.table_data = common.EXAMPLE_DATA.copy()


r.on_update(update)

r.start()