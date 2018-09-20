import gensim
import numpy as np
import multiprocessing


class WordEmbedding:
    """
    Word Embedding class :
        - word2vec
        - doc2vec
    """

    def __init__(self, texts, embedding_dim):
        self.texts = texts
        self.embedding_dim = embedding_dim

    def embed(self, model, word):
        """It the word is not in embedding, return the zero vector."""
        try:
            return model.wv.get_vector(word)
        except KeyError:
            return np.zeros([self.embedding_dim], dtype=np.float32)

    def get_w2v_embedding(self):
        """Return the word2vec embeddings."""

        model = gensim.models.Word2Vec(
            self.texts,
            size=self.embedding_dim,
            window=5,
            sg=1,
            alpha=0.0001,
            min_alpha=0.00005,
            min_count=5,
            workers=multiprocessing.cpu_count()
        )

        print("Word2vec model created.")

        embeddings = [
            np.array([self.embed(model, word) for word in text]) for text in self.texts
        ]

        return np.array(embeddings)

    def get_d2v_model(self):
        """Return the doc2vec embeddings."""

        # Basically, used the ordering of texts.
        documents = LabeledDocument(self.texts, list(range(len(self.texts))))

        model = gensim.models.Doc2Vec(
            documents,
            size=self.embedding_dim,
            window=5,
            alpha=0.0001,
            min_alpha=0.00005,
            epochs=30,
            workers=multiprocessing.cpu_count()
        )

        print("Doc2vec model created.")

        embeddings = [
            np.array([self.embed(model, word) for word in text]) for text in self.texts
        ]

        return np.array(embeddings)


class LabeledDocument(object):
    """Text_ids can be customized."""

    def __init__(self, texts, text_ids):
        self.texts = texts
        self.text_ids = text_ids

    def __iter__(self):
        for idx, text in enumerate(self.texts):
            yield gensim.models.doc2vec.TaggedDocument(words=text, tags=[self.text_ids[idx]])
