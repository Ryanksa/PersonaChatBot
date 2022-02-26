import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel

# Using transformer model and code from https://huggingface.co/af1tang/personaGPT
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


def converse(dialog, persona):
    """
    @param dialog: List of string representing the chat history so far
    @param personas: List of string to specify the chatbot's personality
    @return: chatbot's message
    """
    # encode dialog
    dialog_hx = []
    for text in dialog:
        dialog_hx.append(tokenizer.encode(text + tokenizer.eos_token))

    # encode persona
    personas = tokenizer.encode(
        ''.join(['<|p2|>'] + persona + ['<|sep|>'] + ['<|start|>']))

    # compute chatbot's response
    bot_input_ids = to_var([personas + flatten(dialog_hx)]).long()
    encoded_msg = generate_next(bot_input_ids)
    msg = tokenizer.decode(encoded_msg, skip_special_tokens=True)
    return msg
