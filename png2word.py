import win32com.client as win32

def AddTextBoxToWordDocument(outputs, page_width, page_height, image_width, image_height, dir_path, file_name):
    word_app = win32.gencache.EnsureDispatch('Word.Application')
    word_app.Visible = True

    doc = word_app.Documents.Add()

    page_setup = doc.PageSetup
    page_setup.PageWidth = page_width
    page_setup.PageHeight = page_height

    width_scale = page_width / image_width
    height_scale = page_height / image_height

    for output in outputs:
        scaled_x = output.x * width_scale
        scaled_y = output.y * height_scale
        scaled_width = output.width * width_scale
        scaled_height = output.height * height_scale

        tb = doc.Shapes.AddTextbox(
            Orientation=1,
            Left=scaled_x,
            Top=scaled_y,
            Width=scaled_width,
            Height=scaled_height
        )
        tb.TextFrame.TextRange.Text = output.text
        tb.TextFrame.AutoSize = 1
        tb.Line.Visible = False

    doc.SaveAs(f"{dir_path}\\{file_name}.docx")

    doc.Close()
    word_app.Quit()