import gradio as gr
import numpy as np
import GateWayMain as gw
import mongodb as db
import testOCR as OCR

def checkin(im,ID):
    #### Do sth and return ID
    #ID = 16122002
    Info = db.getInfo(ID)
    if Info is None:
        greeting = 'Stranger detected !!!!'
        return np.flipud(im), greeting
    else:
        gw.FaceReg_In(ID)
        greeting =  f"Welcome back, {Info['name']} !!"

    return np.flipud(im), greeting

def checkout(im,ID):
    #ID = 16122002
    
    Info = db.getInfo(ID)
    if Info is None:
        greeting = 'Stranger detected !!!!'
        return np.flipud(im), greeting
    else:
        gw.FaceReg_Out(ID)
        greeting =  f"Goodbye, {Info['name']} !!"

    return np.flipud(im), greeting


# demo = gr.Interface(
#     flip, 
#     inputs = input,
#     outputs= gr.Image(),
#     #live=True
# )



with gr.Blocks(css=".input_image { max-width: 800; max-height: none; }") as demo:
    with gr.Tab("Demo Recognition: "):
        with gr.Row():
            with gr.Column():
                img_in = gr.Image(source="webcam", streaming=True)
                text = gr.Text(placeholder="ID here")
                with gr.Row():
                    Checkin_btn = gr.Button("Check in")
                    Checkout_btn = gr.Button("Check out")
            with gr.Column():
                imgout = gr.Image()
                textout = gr.Text()
    
    with gr.Tab("OCR Image"):
            with gr.Row():
                image_input = gr.Image().style(width=1000)
                text_output = gr.Text()
            image_button = gr.Button("SUBMIT")

    
    
    Checkin_btn.click(checkin, inputs = [img_in,text], outputs=[imgout,textout])
    Checkout_btn.click(checkout, inputs = [img_in,text], outputs=[imgout,textout])
    
    image_button.click(OCR.TextLineBox ,inputs=image_input, outputs = text_output)


demo.launch()

