from transformers import pipeline

# Load the entailment model
entailment_pipeline = None

def check_entailment(sentence1, sentence2):
    global entailment_pipeline
    if entailment_pipeline is None:
        entailment_pipeline = pipeline("text-classification", model="facebook/bart-large-mnli", device=0)

    result = entailment_pipeline(f"{sentence1} entails {sentence2}")
    label = result[0]['label'].lower()
    score = result[0]['score']
    is_entailment = label == 'entailment'
    return is_entailment, score

if __name__ == "__main__":
    # Example usage
    sentence1 = "The dog is running."
    sentence2 = "The house is running."

    entailment, score = check_entailment(sentence1, sentence2)
    print(f"Entailment: {entailment}, Score: {score}")