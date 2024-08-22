# import openai
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('GPT_KEY')

def add_punctuation(text):
    # Define the prompt to instruct GPT-4
    prompt = (
        "Please add punctuation to the following text, the text is in Japanese:\n\n"
        f"{text}\n\n"
        "Punctuated text:"
    )
    client = OpenAI(
        # This is the default and can be omitted
        api_key=api_key,
    )

    # chat_completion = client.chat.completions.create(
    #     messages=[
    #         {
    #             "role": "user",
    #             "content": prompt,
    #
    #         }
    #     ],
    #     model="gpt-4",
    #
    # )
    # Make the API call to GPT-4
    # response = openai.Completion.create(
    #     engine="gpt-4",  # Specify the model
    #     prompt=prompt,
    #     max_tokens=500,  # Adjust this value based on the length of the text
    #     temperature=0.2,  # Lower temperature for more precise responses
    #     top_p=1.0,
    #     frequency_penalty=0.0,
    #     presence_penalty=0.0
    # )

    messages = [
        {"role": "system", "content": "You are an assistant that helps with text formatting in Japanese."},
        # {"role": "user", "content": f"Please add punctuation to the following text, the text is in Japanese:\n\n{text}\n\nPunctuated text:"}
        {"role": "user", "content": f"Please add punctuation to the following text, or change the current punctuation if not appropriate, the text is in Japanese:\n\n{text}\n\nPunctuated text:"}
    ]

    # Make the API call to GPT-4
    response = client.chat.completions.create(
        # model="gpt-4",  # Specify the model
        model="gpt-4o",  # Specify the model
        messages=messages,
        max_tokens=500,  # Adjust this value based on the length of the text
        temperature=0.2,  # Lower temperature for more precise responses
    )

    # Extract the punctuated text from the response
    # punctuated_text = response.choices[0].text.strip()
    # dump(response.choices[0].message.content)
    # punctuated_text = response.choices[0].message['content'].strip()
    punctuated_text = response.choices[0].message.content
    return remove_first_last_quotes(punctuated_text)

def remove_first_last_quotes(text):
    # Check if the text starts and ends with Japanese quotes
    if text.startswith("「") and text.endswith("」"):
        # Remove the first and last characters
        text = text[1:-1]
    return text

if __name__ == '__main__':
    # Input text with missing punctuation
    text_to_punctuate = "はいではですね第1回目情報セキュリティとはというタイトルで始めさせていただきます目次の説明ですけれどもまずはじめにということで今の情報セキュリティを取り巻く状況てるのということになっているかという点を共有させていただければと考えておりますそして2点目情報セキュリティとはということの本質についてちょっと語りたいと考えておりますで3点目実際に情報セキュリティいたのは事故がよく起きるものでそれはどういう形で何が起きているのかという点に触れて参りますそして4点目情報セキュリティにおいてですね準備をしていただきたいことということで触れてますそして5点目最も重要なことなんでしょうかということについて最後まとめという意味も含めてですね以上いくつの構成で進めさせていただきます"

    # Call the function to add punctuation
    punctuated_text = add_punctuation(text_to_punctuate)

    # Output the result
    print("Original Text:")
    print(text_to_punctuate)
    print("\nPunctuated Text:")
    print(punctuated_text)