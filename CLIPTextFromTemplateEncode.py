
import csv
import os
import sys


#sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), "comfy"))


import comfy.utils


def clip_prompt(clip, text):
    tokens = clip.tokenize(text)
    cond, pooled = clip.encode_from_tokens(tokens, return_pooled=True)
    return [[cond, {"pooled_output": pooled}]]


class ClipTextFromTemplateEncode:

    styles = None

    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(cls):
        template_file_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        template_file = os.path.join(template_file_path, "styles.csv")

        if not os.path.exists(template_file):
            print("WARNING styles.csv does not exist - ClipTextFromTemplateEncode cannot be used")
            cls.styles = [["No Styles.csv", "(((Cartoon sad face))) negativity", "positivity"]]
        else:
            with open(template_file, "r") as f:
                reader = csv.reader(f, dialect='excel')
                #cls.styles = [row for row in reader if row[1]!="prompt" and row[0]!= "None"]
                cls.styles = [row for row in reader if len(row) == 3 and row[1] != "prompt" and row[0] != "None"]


        #print(cls.styles)

        style_names = [row[0] for row in cls.styles]

        return {
            "required": {
                "prompt": ("STRING", {"multiline": True, "default": "Perfect landcape"}),
                "style": (style_names, {"default": style_names[0]}),
                "clip" : ("CLIP",)
            },
        }

    RETURN_TYPES = ("CONDITIONING", "CONDITIONING")
    RETURN_NAMES = ("positive", "negative")
    FUNCTION = "condition"
    OUTPUT_NODE = False
    CATEGORY = "conditioning"

    def condition(self, prompt, style, clip):
        positive=""
        negative=""
        for row in self.styles:
            if row[0] == style:
                positive = row[1]
                if "{prompt}" not in positive:
                    positive =  prompt + " " + positive
                else:
                    positive = positive.replace("{prompt}", prompt)
              
                negative = row[2]

        return (clip_prompt(clip, positive), clip_prompt(clip, negative), )

NODE_CLASS_MAPPINGS = {
    "ClipTextFromTemplateEncode": ClipTextFromTemplateEncode
}
