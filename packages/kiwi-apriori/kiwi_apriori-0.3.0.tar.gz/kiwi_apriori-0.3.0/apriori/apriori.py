import itertools

from apriori.apriori_types import *
from apriori.transaction import Transactions, apriori_from_transaction
from apriori.rule import AssociationRule


def generate_rules_from_transaction(transaction_object: Transactions, min_support:float=0.0,
                   min_confidence:float=0.0, min_lift:float=0.0) -> Iterable[AssociationRule]:
    for freq_set, support in apriori_from_transaction(transaction_object, min_support):
        for base_length in range(1, len(freq_set)):
            for combination_set in itertools.combinations(freq_set, base_length):
                items_base = frozenset(combination_set)
                items_leads_to = frozenset(freq_set - items_base)
                confidence = support[freq_set] / support[items_base]
                lift = confidence / support[items_leads_to]
                if confidence < min_confidence:
                    continue
                if lift < min_lift:
                    continue
                # print(f"Support for {freq_set} is {support[freq_set]}")
                # print(f"All support is {support}")
                yield AssociationRule(base=items_base, leads_to=items_leads_to, confidence=confidence,
                                      support=support[freq_set], lift=lift)


def generate_rules(data: Iterable[Iterable[ItemLabel]], min_support:float,
                   min_confidence:float=0.0, min_lift:float=0.0) -> Iterable[AssociationRule]:
    transaction = Transactions(data)
    return generate_rules_from_transaction(transaction, min_support, min_confidence, min_lift)