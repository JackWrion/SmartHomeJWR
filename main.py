import gradio as gr
import numpy as np
import GateWayMain as gw
import mongodb as db


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




def regis(image_input, name_input, ID_input):
    
    Info = db.getInfo(ID_input)

    if Info is None:
        greeting = f'Register Successfully !!!!\nWelcome {name_input}!!!'
        gw.Register(ID_input)
        return db.addMember(image_input, name_input, ID_input), greeting
    else:
        greeting =  f"Sorry, This ID [{ID_input}] already exists !!!"
        return image_input, greeting





def clear():
    return None, None,None,None
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
    
    Checkin_btn.click(checkin, inputs = [img_in,text], outputs=[imgout,textout])
    Checkout_btn.click(checkout, inputs = [img_in,text], outputs=[imgout,textout])


    with gr.Tab("Register: "):
            with gr.Row():
                with gr.Column():
                    image_input = gr.Image(source="webcam", streaming=True)
                    name_input = gr.Text(label="Name:")
                    ID_input = gr.Text(label="ID:")
                with gr.Column():
                    img_out = gr.Image()
                    text_out = gr.Text()

            with gr.Row():
                reg_button = gr.Button("SUBMIT")
                clear_button = gr.Button("CLEAR")

    
    reg_button.click(regis, inputs= [image_input, name_input, ID_input], outputs= [img_out,text_out])
    clear_button.click(clear, inputs= None , outputs= [name_input, ID_input, img_out, text_out] )
    
    
    


demo.launch()

