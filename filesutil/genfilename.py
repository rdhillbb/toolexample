import sys
sys.path.append("../")
from util.genutil import creatflnprompt
from filesutil.utiltag  import get_tag_text
from llms.llmanthropic import anthropic_llm 
def clean_string(text):
    return text.replace('\n', '').replace('\t', '').strip()
def create_filename(text: str) -> str:
    print("GENFILE", text)
    if len(text) > 200:
        text = text[:200]
    try:
        text = clean_string(text)
        promptfln = creatflnprompt(text)
        result = anthropic_llm(creatflnprompt(promptfln))
        print("*+"*30)
        print("File name",result)
        print("===="*30)
        print()
        tag = get_tag_text(result)
        return tag
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""
    
    return msg

# This print statement should be at the top level, not inside any function or class.
"""
text = "Garlic is a polyphenolic and organosulfur enriched nutraceutical spice consumed since ancient times. Garlic and its secondary metabolites have shown excellent health-promoting and disease-preventing effects on many human common diseases, such as cancer, cardiovascular and metabolic disorders, blood pressure, and diabetes, through its antioxidant, anti-inflammatory, and lipid-lowering properties, as demonstrated in several in vitro, in vivo, and clinical studies. The present review aims to provide a comprehensive overview on the consumption of garlic, garlic preparation, garlic extract, and garlic extract-derived bioactive constituents on oxidative stress, inflammation, cancer, cardiovascular and metabolic disorders, skin, bone, and other common diseases. Among the 83 human interventional trials considered, the consumption of garlic has been reported to modulate multiple biomarkers of different diseases; in addition, its combination with drugs or other food matrices has been shown to be safe and to prolong their therapeutic effects. The rapid metabolism and po"

print(genfilename(text))
"""
