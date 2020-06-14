from com.sun.star.table import BorderLine2

def configureBorders(doc, text, items):
    no_line = BorderLine2()
    no_line.Color = 0
    no_line.InnerLineWidth = 0
    no_line.LineDistance = 0
    no_line.LineStyle = 0
    no_line.LineWidth = 0
    no_line.OuterLineWidth = 0
    text_tables = doc.getTextTables()
    get_top_table = text_tables.getByIndex(0)
    table_top_border = get_top_table.TableBorder
    table_top_border.LeftLine = no_line
    table_top_border.RightLine = no_line
    table_top_border.TopLine = no_line
    table_top_border.BottomLine = no_line
    table_top_border.HorizontalLine = no_line
    table_top_border.VerticalLine = no_line
    get_top_table.TableBorder = table_top_border
    get_middle_table =  text_tables.getByIndex(1)
    table_middle_border = get_middle_table.TableBorder
    table_middle_border.LeftLine = no_line
    table_middle_border.RightLine = no_line
    table_middle_border.TopLine = no_line
    table_middle_border.BottomLine = no_line
    table_middle_border.HorizontalLine = no_line
    table_middle_border.VerticalLine = no_line
    get_middle_table.TableBorder = table_middle_border
    get_main_table =  text_tables.getByIndex(2)
    count = 0
    col = ['A', 'B', 'C', 'D']
    for i in items:
        count = count + 1

    for i in col:
        table_main_cell = get_main_table.getCellByName(i + str(count+2))
        left_border_a_cell = table_main_cell.LeftBorder
        left_border_a_cell.OuterLineWidth = 0
        left_border_a_cell.LineWidth = 0
        table_main_cell.LeftBorder = left_border_a_cell

    cRange = get_main_table.getCellRangeByName("A" + str(count +2) + ":D" + str(count + 2))
    cRange.setPropertyValue( "CharFontName", "Liberation Serif" )
    cRange.setPropertyValue( "CharHeight", 10.0 )
    table_main_cell = get_main_table.getCellByName("D" + str(count+2))
    right_border_a_cell = table_main_cell.RightBorder
    right_border_a_cell.OuterLineWidth = 0
    right_border_a_cell.LineWidth = 0
    table_main_cell.RightBorder = right_border_a_cell
    table_main_border = get_main_table.TableBorder
    table_main_border.BottomLine = no_line
    get_main_table.TableBorder = table_main_border
    get_bottom_table =  text_tables.getByIndex(3)
    table_bottom_border = get_bottom_table.TableBorder
    table_bottom_border.Distance = 50
    table_bottom_border.HorizontalLine = no_line
    table_bottom_border.VerticalLine = no_line
    get_bottom_table.TableBorder = table_bottom_border
    return doc, text
