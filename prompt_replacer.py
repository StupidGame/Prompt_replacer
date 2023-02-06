import modules.scripts as scripts
import gradio as gr
import os
import csv

from modules import images
from modules.processing import process_images, Processed
from modules.processing import Processed
from modules.shared import opts, cmd_opts, state

def apply_prompt(prompt, replace_prompt, negative_prompt):
    f = open('replacer.csv', 'r')
    
    if(os.path.isfile('replacer.csv')):
        f = open('replacer.csv', 'a', newline="")
    else:
        f = open('replacer.csv', 'w', newline="")
    writer = csv.writer(f)
    writer.writerow([prompt, replace_prompt, negative_prompt])
    f.close()

def read_csv(filename):
    f = open(filename, 'r')
    reader = csv.reader(f)
    list = [row for row in reader]
    return list


class Script(scripts.Script):  

# The title of the script. This is what will be displayed in the dropdown menu.
    def title(self):
        return "prompt replacer"

    def ui(self, is_img2img):
        csvframe = gr.DataFrame(value=read_csv('replacer.csv'), max_rows=3, wrap=True)
        base_text = gr.Textbox(label="base prompt",placeholder="type base prompt")
        replace_text = gr.Textbox(label="replace prompt",placeholder="type replace prompt")
        negative_text = gr.Textbox(label="replace negative prompt",placeholder="type replace negative prompt")
        button = gr.Button(value="save")
        button.click(apply_prompt, inputs=[base_text, replace_text, negative_text])
        return [csvframe, base_text, replace_text, negative_text, button]
    
    def run(self, p, csvframe, base_text, replace_text, negative_text, button):
        f = open('replacer.csv', 'r')
        reader = csv.reader(f)
        for low in reader:
            if(low[0] in p.prompt):
                p.prompt = p.prompt.replace(low[0], low[1])
                p.negative_prompt += low[2]
        proc = process_images(p)
        p.do_not_save_samples = True
        f.close()
        for i in range(len(proc.images)):
            images.save_image(proc.images[i], p.outpath_samples, "replaced",
            proc.seed + i, proc.prompt, opts.samples_format, info= proc.info, p=p)