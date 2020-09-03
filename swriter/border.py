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
    try :
        hospital_table = text_tables.getByName('hospital_table')
        hospital_table_border = hospital_table.TableBorder
        hospital_table_border.LeftLine = no_line
        hospital_table_border.VerticalLine = no_line
        hospital_table_border.HorizontalLine = no_line
        hospital_table_border.BottomLine = no_line
        hospital_table_border.TopLine = no_line
        hospital_table_border.RightLine = no_line
        hospital_table.TableBorder = hospital_table_border
    except Exception:
        pass
    get_top_table = text_tables.getByName('identity_table')
    table_top_border = get_top_table.TableBorder
    table_top_border.LeftLine = no_line
    table_top_border.RightLine = no_line
    table_top_border.TopLine = no_line
    table_top_border.BottomLine = no_line
    table_top_border.HorizontalLine = no_line
    table_top_border.VerticalLine = no_line
    get_top_table.TableBorder = table_top_border
    get_middle_table =  text_tables.getByName('patient_table')
    table_middle_border = get_middle_table.TableBorder
    table_middle_border.LeftLine = no_line
    table_middle_border.RightLine = no_line
    table_middle_border.TopLine = no_line
    table_middle_border.BottomLine = no_line
    table_middle_border.HorizontalLine = no_line
    table_middle_border.VerticalLine = no_line
    get_middle_table.TableBorder = table_middle_border
    try :
        get_diagnosis_table = text_tables.getByName('diagnosis_table')
        otabseps = get_diagnosis_table.TableColumnSeparators
        relativeTableWidth = get_diagnosis_table.getPropertyValue( "TableColumnRelativeSum" )
        otabseps[0].Position = 1675
        otabseps[1].Position = 6670
        otabseps[2].Position = 8330
        get_diagnosis_table.TableColumnSeparators = otabseps
        get_diagnosis_table.setPropertyValue("TableColumnSeparators", otabseps)
        table_diagnosis_border = get_diagnosis_table.TableBorder
        table_diagnosis_border.LeftLine = no_line
        table_diagnosis_border.RightLine = no_line
        table_diagnosis_border.TopLine = no_line
        table_diagnosis_border.BottomLine = no_line
        table_diagnosis_border.VerticalLine = no_line
        table_diagnosis_border.HorizontalLine = no_line
        get_diagnosis_table.TableBorder = table_diagnosis_border
    except Exception:
        pass
    get_main_table =  text_tables.getByName('treatment_table')
    count = 0
    col = ['A', 'B', 'C', 'D', 'E']
    for i in items:
        count = count + 1
    for i in range(len(col)):
        table_main_cell = get_main_table.getCellByPosition(i,(count+1))
        left_border_a_cell = table_main_cell.LeftBorder
        left_border_a_cell.OuterLineWidth = 0
        left_border_a_cell.LineWidth = 0
        table_main_cell.LeftBorder = left_border_a_cell

    cRange = get_main_table.getCellRangeByName("A" + str(count +2) + ":E" + str(count + 2))
    cRange.setPropertyValue( "CharFontName", "Liberation Serif" )
    #cRange.setPropertyValue( "CharHeight", 10.0 )
    table_main_cell = get_main_table.getCellByName("E" + str(count+2))
    right_border_a_cell = table_main_cell.RightBorder
    right_border_a_cell.OuterLineWidth = 0
    right_border_a_cell.LineWidth = 0
    table_main_cell.RightBorder = right_border_a_cell
    table_main_border = get_main_table.TableBorder
    table_main_border.BottomLine = no_line
    get_main_table.TableBorder = table_main_border


    get_bottom_table =  text_tables.getByName('footer_table')
    table_bottom_border = get_bottom_table.TableBorder
    table_bottom_border.Distance = 50
    table_bottom_border.HorizontalLine = no_line
    table_bottom_border.VerticalLine = no_line
    get_bottom_table.TableBorder = table_bottom_border
    return doc, text
