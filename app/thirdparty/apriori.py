"""
Description     : Simple Python implementation of the Apriori Algorithm
"""

import logging
from models import AssociationRuleModel

from itertools import chain, combinations
from collections import defaultdict

MIN_CONFIDENCE = 0.6
MIN_SUPPORT = .15
MAX_K = 4
MAX_TXN_SIZE = 5
MIN_PREF_MEAN = .05  # Filters out "trolls"


def subsets(arr):
    """ Returns non empty subsets of arr"""
    return chain(*[combinations(arr, i + 1) for i, a in enumerate(arr)])


def returnItemsWithMinSupport(item_set, txn_list, min_support, freq_set):
    """calculates the support for items in the itemSet and returns a subset
    of the itemSet each of whose elements satisfies the minimum support"""

    # Default histograms
    _itemSet = set()
    localSet = defaultdict(int)

    # Iterate over item set and update histogram data
    for item in item_set:
        for transaction in txn_list:
            if item.issubset(transaction):
                freq_set[item] += 1
                localSet[item] += 1

    # Calculate support
    total_txns = len(txn_list)
    for item, count in localSet.items():
        support = float(count) / total_txns

        if support >= min_support:
            _itemSet.add(item)

    return _itemSet


def joinSet(item_set, length):
        """Join a set with itself and returns the n-element itemsets"""
        # This could use some profiling...
        return set([i.union(j) for i in item_set for j in item_set if len(i.union(j)) == length])


def get_item_set_transaction_list(dataset_iter):
    """
    Given a list of tuples of variable length, yield a unique itemset and transaction list
    """
    logging.error(len(dataset_iter))
    txn_list = list()
    item_set = set()

    for record in dataset_iter:
        record_mean = 0
        for item in record:
            if item[-1] == '1':
                record_mean = record_mean + 1
        record_mean = float(record_mean) / float(len(record))

        # Filter out people who only dislike things
        logging.error([record_mean, len(record)])
        if record_mean < MIN_PREF_MEAN:
            logging.error('skipping....')
            continue

        batches = list(batcher(record, MAX_TXN_SIZE))

        for batch in batches:
            txn = frozenset(batch)
            txn_list.append(txn)
            for item in txn:
                item_set.add(frozenset([item]))  # Generate 1-itemSets
    return item_set, txn_list


def batcher(l, n):
    # Split a list into smaller lists of max-length n

    # For item i in a range that is a length of l,
    for i in range(0, len(l), n):
        # Create an index range for l of n items:
        yield l[i:i+n]


def runApriori(dataset_iter, min_support, min_confidence):
    """
    run the apriori algorithm. data_iter is a record iterator
    Return both:
     - items (tuple, support)
     - rules ((pretuple, posttuple), confidence)
    """

    itemSet, transactionList = get_item_set_transaction_list(dataset_iter)

    freqSet = defaultdict(int)
    largeSet = dict()
    # Global dictionary which stores (key=n-itemSets,value=support)
    # which satisfy minSupport

    # assocRules = dict() //cruft?
    # Dictionary which stores Association Rules

    logging.error('returnItemsWithMinSupport')
    oneCSet = returnItemsWithMinSupport(itemSet,
                                        transactionList,
                                        min_support,
                                        freqSet)

    # TODO: This could be done in a deferred task?
    # k = 1 => {a, b, c, d}
    # k = 2 => {ab, ac, ad, bc, bd, c, d}
    # k = 3 => {abc, abd, acd, bcd}
    currentLSet = oneCSet
    k = 2
    while(currentLSet != set([]) and k <= MAX_K):
        largeSet[k - 1] = currentLSet
        currentLSet = joinSet(currentLSet, k)
        currentCSet = returnItemsWithMinSupport(currentLSet,
                                                transactionList,
                                                min_support,
                                                freqSet)
        currentLSet = currentCSet
        k = k + 1
        logging.error('loooooooooop: ' + str(k))

    total_txns = len(transactionList)

    def getSupport(item):
            """local function which Returns the support of an item"""
            return float(freqSet[item]) / total_txns

    toRetItems = []
    for key, value in largeSet.items():
        toRetItems.extend([(tuple(item), getSupport(item))
                           for item in value])

    logging.error('prior to final nested loop')
    logging.error(largeSet)
    logging.error(len(largeSet.items()))

    toRetRules = []
    for key, value in largeSet.items()[1:]:
        for item in value:
            _subsets = map(frozenset, [x for x in subsets(item)])
            for element in _subsets:
                remain = item.difference(element)
                if len(remain) > 0:
                    confidence = getSupport(item) / getSupport(element)
                    if confidence >= min_confidence:
                        toRetRules.append(((tuple(element), tuple(remain)),
                                           confidence))
    return toRetItems, toRetRules


def printResults(items, rules):
    """prints the generated itemsets sorted by support and the confidence
        rules sorted by confidence"""
    for item, support in sorted(items, key=lambda (item, support): support):
        print "item: %s , %.3f" % (str(item), support)
    print "\n------------------------ RULES:"
    for rule, confidence in rules:  # sorted(rules, key=lambda (rule, confidence): confidence):
        pre, post = rule

        r = AssociationRuleModel(pre, post, confidence)
        print r
