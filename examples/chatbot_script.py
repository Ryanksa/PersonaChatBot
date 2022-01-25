import sys
from transformers import GPT2Tokenizer, GPT2LMHeadModel
import torch
tokenizer = GPT2Tokenizer.from_pretrained("af1tang/personaGPT")
model = GPT2LMHeadModel.from_pretrained("af1tang/personaGPT")
if torch.cuda.is_available():
    model = model.cuda()


def flatten(l): return [item for sublist in l for item in sublist]


def to_data(x):
    if torch.cuda.is_available():
        x = x.cpu()
    return x.data.numpy()


def to_var(x):
    if not torch.is_tensor(x):
        x = torch.Tensor(x)
    if torch.cuda.is_available():
        x = x.cuda()
    return x


def display_dialog_history(dialog_hx):
    for j, line in enumerate(dialog_hx):
        msg = tokenizer.decode(line)
        if j % 2 == 0:
            print(">> User: " + msg)
        else:
            print("Bot: "+msg)
            print()


def generate_next(bot_input_ids, do_sample=True, top_k=10, top_p=.92,
                  max_length=1000, pad_token=tokenizer.eos_token_id):
    full_msg = model.generate(bot_input_ids, do_sample=True,
                              top_k=top_k, top_p=top_p,
                              max_length=max_length, pad_token_id=tokenizer.eos_token_id)
    msg = to_data(full_msg.detach()[0])[bot_input_ids.shape[-1]:]
    return msg


personas = [
    "I am a mature person.",
    "I am caring but get angry at injustices.",
    "I enjoy playing video games and birdwatching.",
]
personas = tokenizer.encode(
    ''.join(['<|p2|>'] + personas + ['<|sep|>'] + ['<|start|>']))


dialog = sys.argv[1:]

dialog_hx = []
for text in dialog:
    dialog_hx.append(tokenizer.encode(text + tokenizer.eos_token))

bot_input_ids = to_var([personas + flatten(dialog_hx)]).long()
encoded_msg = generate_next(bot_input_ids)
dialog_hx.append(encoded_msg)

msg = tokenizer.decode(encoded_msg, skip_special_tokens=True)
print(msg)
sys.stdout.flush()
