import time

def pushMe( event ):
    textBoxModel = event.Source.getModel().getParent().TextBox
    textBoxModel.Text = textBoxModel.Text + "\nyou pushed me (" + time.asctime() + ")"
