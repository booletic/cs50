import nltk


class Analyzer():
    """Implements sentiment analysis."""

    def __init__(self, positives, negatives):
        """Initialize Analyzer."""
        self.positives_list = list()
        file = open(positives, "r")
        for line in file:
            if not line.startswith(';') and line is not '\n':
                self.positives_list.append(line.strip())
        file.close()

        self.negatives_list = list()
        file = open(negatives, "r")
        for line in file:
            if not line.startswith(';') and line is not '\n':
                self.negatives_list.append(line.strip())
        file.close()

    def analyze(self, text):
        """Analyze text for sentiment, returning its score."""
        tokenizer = nltk.tokenize.TweetTokenizer()
        tokens = tokenizer.tokenize(text)
        score = 0

        for token in tokens:
            if token in self.positives_list:
                score += 1
            elif token in self.negatives_list:
                score -= 1

        return score