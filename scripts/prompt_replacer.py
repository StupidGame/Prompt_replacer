import modules.scripts as scripts
import gradio as gr
import os
import csv

from modules import images
from modules.processing import process_images, Processed
from modules.processing import Processed
from modules.shared import opts, cmd_opts, state

# 読み込み
def read_csv():
    f = open('replacer.csv', "r")
    csv_data = csv.reader(f)
    list = [ e for e in csv_data]
    f.close()
    return list

def write_csvdata(dataframe):
    csvdata = dataframe
    with open('replacer.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(csvdata)   

    f.close()

class Script(scripts.Script):  
    if(not os.path.isfile('replacer.csv')):
        f = open('replacer.csv', 'w', newline="")
        writer = csv.writer(f)
        writer.writerow([" ", " ", " "])
        f.close()


# The title of the script. This is what will be displayed in the dropdown menu.
    def title(self):
        return "prompt replacer"

    def ui(self, is_img2img):
        csvlist = read_csv()
        csvframe = gr.DataFrame(value=csvlist, max_rows=3, wrap=True , type="array", interactive=True, col_count=(3, "fixed"))
        button = gr.Button(value="save", variant="primary")
        button.style(full_width=True)
        button.click(write_csvdata, csvframe)
        return [csvframe, button]
    
    def run(self, p, csvframe, button):
        f = open('replacer.csv', 'r')
        reader = csv.reader(f)
        for low in reader:
            if(low[0] in p.prompt):
                p.prompt = p.prompt.replace(low[0], low[1])
                p.negative_prompt = p.negative_prompt + ' , ' + low[2]
        p.do_not_save_samples = False
        f.close()
