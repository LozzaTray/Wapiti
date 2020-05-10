"""Module for performing ofdm tasks"""


def insert_cyclic_prefix(x, K):
    """inserts a cyclic prefix of length K into the data sequence x
    allows linear convolution to match cyclic"""
    raise NotImplementedError


def encode(data_sequence, K):
    """encodes the data_sequence X into the the time sequence x 
    by taking the iDFT and inserting a cyclic prefix of length K"""
    raise NotImplementedError


def decode(received_sequence, channel_impulse_response):
    """decodes by taking the DFT of the received_sequence and channel_impulse_response
    then apply point-wise division to get the true symbol value"""
    raise NotImplementedError