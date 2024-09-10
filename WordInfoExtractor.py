import pandas as pd
from openai import OpenAI

_ = load_dotenv(find_dotenv())
client = OpenAI(api_key="OPENAI_API_KEY")
# Function to ask GPT for the part of speech, meaning, and example sentence of a word

def ask_gpt(word):
    # This function sends a request to GPT to get the part of speech, meaning, and example sentence for the word
    response = client.chat.completions.create(
        model="gpt-4",  # Adjust the model to the appropriate version like 'gpt-4' or 'gpt-3.5-turbo'
        messages=[
            {
                'role': 'system',
                'content': (
                    'You are an English language expert who gives direct, to-the-point answers. '
                    'When the user asks you the part of speech, meaning, and sentence for a word, you directly provide it. '
                    'For example:\n'
                    'user: Give the part of speech, meaning, and sentence for the word affront?\n'
                    'assistant: Noun, An action or remark that causes outrage or offense. '
                    'Example sentence: His rude behavior was an affront to everyone in the room.'
                )
            },
            {
                'role': 'user',
                'content': f'Give the part of speech, meaning, and sentence for the word {word}.'
            }
        ]
    )
    
    # Extracting the response from GPT
    answer = response.choices[0].message.content.strip()
    return answer

# Read the CSV file containing the list of words into a Pandas DataFrame
df = pd.read_csv('word_list.csv')

# Add new columns to the DataFrame for part of speech, meaning, and sentence
df['Part of Speech'] = ''
df['Meaning'] = ''
df['Example Sentence'] = ''

# Iterate through each row in the DataFrame
for index, row in df.iterrows():
    word = row['Word']  # Get the word from the row

    # Get the part of speech, meaning, and sentence by calling the ask_gpt function
    result = ask_gpt(word)
    
    # Split the result (assuming it returns in the form "Part of Speech, Meaning. Example Sentence: ...")
    try:
        # Extract part of speech, meaning, and example sentence
        part_of_speech, rest = result.split(",", 1)  # Get part of speech and the rest
        meaning, sentence = rest.split("Example sentence:", 1)  # Split meaning and sentence
        
        # Update the DataFrame with the part of speech, meaning, and example sentence
        df.at[index, 'Part of Speech'] = part_of_speech.strip()
        df.at[index, 'Meaning'] = meaning.strip()
        df.at[index, 'Example Sentence'] = sentence.strip()
    
    except ValueError:
        # If GPT response is in an unexpected format, leave the fields blank or handle appropriately
        print(f"Error processing word: {word}")

    # Print for monitoring progress
    print(f"Word: {word}\nPart of Speech: {part_of_speech.strip()}\nMeaning: {meaning.strip()}\nSentence: {sentence.strip()}\n")

# Save the updated DataFrame to an Excel file
df.to_excel('word_details_output.xlsx', index=False)

print("Completed updating the meanings.")
