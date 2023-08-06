from apriori.apriori_types import SetLike
import pydantic


class AssociationRule(pydantic.BaseModel):
    """Rules for association, such as {'sugar', 'spice'} -> {'flour'}

    More generally we will write A --> B. Note P(A) is the probability that A is a subset
    of a transaction. Note this weird convention means if A and B are BOTH subsets, then we
    have P(A AND B subsets) = P(A U B) <= P(A) or P(B) [which messes with normal intuition!]

    support of rule:        P(A U B)      i.e. Probability of A U B appearing in a transaction
    confidence in a rule:   P(B | A)      i.e. We know A was included, what is the probability of B
    lift of a rule:         P(B | A)/P(B) = P(A and B)/(P(A)P(B))
                                          i.e. 1 if A and B are independent, greater than 1 if A leads to
                                               more occurrences of B than expected by chance
    """
    base: SetLike
    leads_to: SetLike
    support: float
    confidence: float
    lift: float

    def format_rule(self) -> str:
        def format_setlike(s):
            return '{' + ','.join(sorted([str(element) for element in s])) + '}'
        return f'{format_setlike(self.base)} ---> {format_setlike(self.leads_to)}'