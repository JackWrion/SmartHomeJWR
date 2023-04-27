import gradio as gr
import GateWayMain as gw
import mongodb as db
import AI
import cv2
import random


gw.accessPort()

def checkin(im,ID):
    
    ## Client --> AI --> DB --> Gateway --> Done


    ## Detect with AI first

    name = "./cache/" + str(ID) + "_" + "111111" + ".jpg"
    image_input = cv2.cvtColor(im,cv2.COLOR_RGB2BGR)
    cv2.imwrite(name, image_input)

    face_path = AI.Verification(name)

    if face_path == "None" or  face_path == "Error":
        greeting = 'Stranger detected !!!!'
        return im, greeting, None


    ## parse ID of face detected and compare with input ID 

    face_parse = face_path.replace("./member_image/","")
    face_parse = face_parse.split('_')

    userID = face_parse[1]
    username = face_parse[0]

    if userID == ID:
        # check in DATABASE if user outdoor
        status = db.checkin(ID_input=userID, name_input=username)
        if status == 0:
            # Update to MQTT
            gw.FaceReg_In(ID)
            greeting =  f"Welcome back, {username} !!!"
        else:
            greeting =  f"You are already in, {username} !\nMaybe, You want to check-out....??"
        
    else:
        greeting = 'Wrong ID, please try again !!!!'


    return im, greeting, None



def checkout(im,ID):
    #ID = 16122002
    
    # detect with  __AI__  first

    name = "./cache/" + str(ID) + "_" + "111111" + ".jpg"
    image_input = cv2.cvtColor(im,cv2.COLOR_RGB2BGR)
    cv2.imwrite(name, image_input)

    face_path = AI.Verification(name)

    if face_path == "None" or face_path == "Error":
        greeting = 'Stranger detected !!!!'
        return im, greeting, None

    face_parse = face_path.replace("./member_image/","")
    face_parse = face_parse.split('_')

    userID = face_parse[1]
    username = face_parse[0]


    ## Check in DB
    if userID == ID:
        status,count = db.checkout(ID_input=userID, name_input=username)

        if status == 0:

            ## Update to MQTT
            gw.FaceReg_Out(ID, count)
            greeting =  f"See you soon, {username} !!!"
        else:
            greeting =  f"You are already out, {username} !\nMaybe, You want to check-in....??"

    else:
        greeting = 'Wrong ID, please try again !!!!'

    return im, greeting, None



# def regis(imageinput, name_input, ID_input):
    
#     Info = db.getInfo(ID_input)

#     #name = "./cache/" +str(name_input) +"_"+ str(ID_input) + "_" + "000000" + ".jpg"
#     image_input = cv2.cvtColor(imageinput,cv2.COLOR_RGB2BGR)

#     if Info is None:
#         name = "./member_image/" +str(name_input) +"_"+ str(ID_input) + "_" + "000000" + ".jpg"
#         cv2.imwrite(name, image_input)

#         AI.register(name_input= name_input,ID=ID_input)

#         greeting = f'Register Successfully !!!!\nWelcome {name_input}!!!'
        
#         gw.Register(ID_input)               ## Create feed named by ID
#         db.addMember(name, name_input, ID_input)   ## Create log member

#         return imageinput , greeting
    
#     else:

#         greeting =  f"Sorry, This ID [{ID_input}] already exists !!!\nThe image will be added to improve verification !!!"
#         id = random.randint(0,999999)
#         name = "./member_image/" +str(name_input) +"_"+ str(ID_input) + "_" + str(id) + ".jpg"
#         cv2.imwrite(name, image_input)
#         AI.register(name_input= name_input,ID=ID_input)

#         return imageinput, greeting



# def clear():
#     return None, None,None,None

   


with gr.Blocks(theme='gstaff/xkcd@0.0.1') as demo:
    with gr.Tab("Demo Recognition: "):
        with gr.Row():
            with gr.Column():
                #img_in = gr.Image(source="webcam", streaming=True)
                img_in = gr.Image(source="upload")
                text = gr.Text(placeholder="ID here")
                with gr.Row():
                    Checkin_btn = gr.Button("Check in")
                    Checkout_btn = gr.Button("Check out")
                    
            with gr.Column():
                imgout = gr.Image().style(height=500)
                textout = gr.Text()
        
        #demo_button = gr.Button("DEMO").style(css="background-color: orange")

    Checkin_btn.click(checkin, inputs = [img_in,text], outputs=[imgout,textout,text])
    Checkout_btn.click(checkout, inputs = [img_in,text], outputs=[imgout,textout,text])


    with gr.Tab("Recognition Streaming: "):
        with gr.Row():
            with gr.Column():
                img_in2 = gr.Image(source="webcam", streaming=True).style(height=500)
                text2 = gr.Text(placeholder="ID here")
                with gr.Row():
                    Checkin_btn2 = gr.Button("Check in")
                    Checkout_btn2 = gr.Button("Check out")
                    
            with gr.Column():
                imgout2 = gr.Image().style(height=500)
                textout2 = gr.Text()
        
    Checkin_btn2.click(checkin, inputs = [img_in2,text2], outputs=[imgout2,textout2,text2])
    Checkout_btn2.click(checkout, inputs = [img_in2,text2], outputs=[imgout2,textout2,text2])




 

if __name__ == '__main__':
    demo.launch(server_port=7800)
