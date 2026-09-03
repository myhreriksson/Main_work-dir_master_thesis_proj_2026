from transformers import (AutoTokenizer, 
                          AutoModelForSeq2SeqLM)
import torch # remember to move to device!
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-m', '--model', help='Path to the NMT model.')
parser.add_argument('-n', '--name', help='Model name, which will be added to translated text.')
parser.add_argument('-i', '--input', help='Path to the source text to be translated.')
parser.add_argument('-o', '--output', help='Path to where the target translation should be saved.')
parser.add_argument('-b', '--beam_size', type=int, help='How many possible predictions the model will consider.')
parser.add_argument('--src_lang', help='The language code for the model\'s source language.')
parser.add_argument('--tgt_lang', help='The language code for the model\'s target language.')
parser.add_argument('--batch_size', default=16, type=int, help='How many sentences should be simultaneously processed.')
arg = parser.parse_args()

# part 1: load model & tokenizer
device = 'cuda' if torch.cuda.is_available() else 'cpu' # device to GPU if possible

tokenizer = AutoTokenizer.from_pretrained(arg.model, src_lang=arg.src_lang)
model = AutoModelForSeq2SeqLM.from_pretrained(arg.model, dtype=torch.float16).to(device)
forced_bos_token_id = tokenizer.convert_tokens_to_ids(arg.tgt_lang)

inp_path = arg.input
out_path = arg.output
os.makedirs(out_path, exist_ok=True)

# part 2: execute translation
def main():
    for inp_file in os.listdir(inp_path):
        media_prefix = inp_file.split('_')[0]
        inp_fullpath = os.path.join(inp_path, inp_file)
        out_fullpath = os.path.join(out_path, f'{media_prefix}_Translation_{arg.name}_EN-DE.txt')
        with (
            open(inp_fullpath, 'r', encoding='utf-8') as i_f, # input file
            open(out_fullpath, 'w', encoding='utf-8') as o_f # output file
            ):
            lines = i_f.readlines() # source lines

            for chunk in range(0, len(lines), arg.batch_size):
                batch = [line.strip() for line in lines[chunk:chunk + arg.batch_size]]

                # 2.1: define input parameters
                inputs = tokenizer(
                    batch,
                    return_tensors='pt',
                    padding=True,
                    truncation=True,
                    max_length=128
                ).to(device)

                # 2.2: generate translations (model inference)
                with torch.inference_mode():
                    translated_tokens = model.generate(
                        **inputs,
                        forced_bos_token_id=forced_bos_token_id,
                        num_beams=arg.beam_size,
                        max_length=128
                    )

                # 2.3: decode generated translations
                translations = tokenizer.batch_decode(
                    translated_tokens,
                    skip_special_tokens=True
                )

                # 2.4: write translations to output file
                for trans in translations:
                    o_f.write(trans.strip() + '\n')
            print(f'Translation successfully executed and saved!')

if __name__=='__main__':
    main()