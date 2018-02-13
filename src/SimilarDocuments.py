import binascii
import numpy as np
import pandas as pd
import time
import random


class SimilarDocuments:

    def __init__(self, desc, k_shingling_size, amount_hash_functions):
        self.k_shingling_size = k_shingling_size
        self.maxShingleID = 2 ** 32 - 1
        self.nextPrime = 4294967311
        self.amount_hash_functions = amount_hash_functions
        self.desc = [d.lower() for d in desc]
        self.coefficient_a = self.generate_coefficients(amount_hash_functions)
        self.coefficient_b = self.generate_coefficients(amount_hash_functions)
        self.amount_of_articles = len(desc)

    # Create the set of strings of length k that appear in the document
    def shingling(self, text):
        tokens = text.split()
        tokens_len = len(tokens)
        token_set = []
        if tokens_len >= self.k_shingling_size:
            token_set = [tokens[i:i + self.k_shingling_size] for i in range(0, tokens_len)]
            token_set = token_set[:-(self.k_shingling_size - 1)]
        token_set_compressed = [(binascii.crc32((" ".join(shingle)).encode(encoding='utf-8')) & 0xffffffff) for shingle
                                in token_set]
        return token_set_compressed

    # MIN HASHING

    def generate_coefficients(self, total):
        coefficients = []
        for i in range(0, total):
            coefficient = random.randint(0, self.maxShingleID)
            while coefficient in coefficients:
                coefficient = random.randint(0, self.maxShingleID)
            coefficients.append(coefficient)
            i += 1
        return coefficients

    def min_Hashing(self, x, a, b):
        hash_signature = []
        for idx in range(0, self.amount_hash_functions):
            min_hash = self.nextPrime + 1
            for shingleID in x:
                hash_value = (self.coefficient_a[idx] * shingleID + self.coefficient_b[idx]) % self.nextPrime
                if hash_value < min_hash:
                    min_hash = hash_value
            hash_signature.append(min_hash)
        return hash_signature

    def compare_Signatures(self, s1, s2):
        position_coincidence_count = 0
        position_coincidence_count = np.sum(s1 == s2)
        distance = float(position_coincidence_count) / self.amount_hash_functions
        return distance

    def build_Signature_Matrix(self):
        print('Building Signature Matrix')
        signature_matrix = np.array(self.min_Hashing(self.shingling(self.desc[0]), self.coefficient_a, self.coefficient_b))
        for i in range(1, self.amount_of_articles):
            signature_row = np.array(self.min_Hashing(self.shingling(self.desc[i]), self.coefficient_a, self.coefficient_b))
            signature_matrix = np.vstack((signature_matrix, signature_row))
        print('The Signature Matrix is Ready!')
        return signature_matrix

    def signature_Similarities(self,signature_matrix):
        t1 = time.time()
        print('Computing Signature Similarities...')
        signature_similarities = np.zeros((self.amount_of_articles, self.amount_of_articles))
        for i in range(0, self.amount_of_articles):
            s1 = signature_matrix[i, :]
            for other_document in range(i + 1, self.amount_of_articles):
                s2 = signature_matrix[other_document, :]
                distance = self.compare_Signatures(s1, s2)
                # could be improved since the matrix should be simetric, e.g.: make it triangular
                signature_similarities[i, other_document] = distance
                signature_similarities[other_document, i] = distance
            if (i % 100 == 0):
                print
                str(i) + " / " + str(self.amount_of_articles)
        print
        'Finished!\nTotal time: ', time.time() - t1
        return signature_similarities



