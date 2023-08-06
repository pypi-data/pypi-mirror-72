# apriori

Pip installable association analysis package.

Our datasets is a list of transactions, individual people that 'purchased'
items together. We are trying to find things that are associated with each other.

## Installation

```bash
pip install apriori
```

## Quick example 

This dataset looks at the purchases of 4 customers:
```python
transactions = [
    ['fish', 'white wine', 'cheese', 'bread'],
    ['beer', 'nachos', 'cheese', 'peanuts'],
    ['white wine', 'cheese'],
    ['white wine', 'cheese', 'bread']
]
```

We are interested in which items are associated with one another. It seems that people that
bought white wine also bought cheese. Here are some "association rules" we find:


| If you buy ... | ... we think you'd like | Support | Confidence | Lift |
| ---- | ---- | --- | ---- | ---- |
| white wine | bread | 0.5000 |  0.6667 |  1.3333 |
| bread | white wine | 0.5000 | 1.0000 | 1.3333 |
| white wine | bread AND cheese | 0.5000 | 0.6667 | 1.3333 |
| bread  | cheese AND white wine| 0.5000 | 1.0000 | 1.3333 |
| cheese AND white wine | bread | 0.5000 | 0.6667 | 1.3333 |
| bread AND cheese | white wine | 0.5000 | 1.0000 | 1.3333|

Let's look at the first two rows to illustrate support, confidence, and lift.

* __Support__: Fractions of transactions containing these items. i.e. the probability a randomly chosen transaction contains all the items.
  - The first two rows are about `{white wine}` and `{bread}`. Half of our transactions contain both these items (`transactions[0]` amd `transactions[3]`)
  - Order doesn't matter, the support of `{white wine}` --> `{bread}` and `{bread}` --> `{white wine}` are the same
  - Can be applied to single items (e.g. support for `{white wine}` is 0.75, as 3/4 transactions contain white wine)
* __Confidence of A --> B__: Fraction of transactions containing A that also contain B. i.e. the probability that a randomly chosen transaction containing A also contains B
  - 2 of the 3 transactions containing `{white wine}` also contain `{bread}`, so confidence of `white wine -> bread` is 0.667 
  - 2 of the 2 transactions containing `{bread}` also contain `{white wine}`, so confidence of `bread -> white wine` is 1.000
  - Can be calculated as `support(A AND B)/support(A)
* __Lift of A --> B__: The support of A AND B divided by the support of A and the support of B
  - Measures the amount of information you get knowing A
  - Knowing the lift of white wine to bread is 1.3333 tells us that someone buying white wine is 1.3333 times more likely than the average person to buy bread as well. 
  - If A and B were independent, Lift would be 1
  - If the lift is less than one, that tells us someone is _less_ likely than the average person to buy the other item.
  
## Quickstart

Taken from [example.py](example.py)
```python
import apriori


sample_transactions = [
    ['fish', 'white wine', 'cheese', 'bread'],
    ['beer', 'nachos', 'cheese', 'peanuts'],
    ['white wine', 'cheese'],
    ['white wine', 'cheese', 'bread']
]

for rule in apriori.generate_rules(sample_transactions, min_support=0.5):
    msg = (f'{rule.format_rule():20s}\t\t'
           f'(support={rule.support:0.4f}, confidence={rule.confidence:0.4f}, lift={rule.lift:0.4f})')
    print(msg)
```

## Alternative approaches

This is one approach to determining "this-goes-with-that". Here are comparisons to other alternatives

### Graph / Network models

We could model each item as a node in a graph, and put a weighted edge between items that appear in the same transaction.
In our example, "white wine" and "cheese" would both be nodes, and be joined by a weight of 3. We could then do a community
detection algorithm to find things that are associated with one another, or look for hubs (items that are associated with a
lot of different purchases).

**Pros**
- Algorithm is a lot faster (much smaller size than this algorithm).

**Cons**
- Edges are formed between pairs of nodes, so this approach tells you about pairs of items that are associated.
  It doesn't find cases like "everyone who bought all three of A, B, and C also bought D".
  
### Matrix Factorization

We are focusing on items that are associated with each other; we can score them by one-hot encoding the different
transactions and finding the dot product between pairs of items. This score will be the number of transactions both
items coexist in.

**Pros**
- A lot faster
- Can be trained online / streaming
- Lots of support

**Cons**
- Popular items have higher scores (can mitigate this using cosine distance)
- Limited to comparing pairs of items (although you can try and make a lower dimensional representation and see which 
  items have a similar representation in this lower dimensional space)
  
### Max-Miner

Unlike the other two algorithms, this one is specifically designed for this problem. It deals with sets of items, not
just pairs of items. It also deals with the drawback of this algorithm being slow.

**Pros**
- A lot faster than apriori
- Deals with sets of items, rather than pairs of items

**Cons**
- Finds most, but not all, association rules

## Other applications

Although the examples have all been framed in terms of items bought in transactions with one another, this algorithm 
can be used to find what sets of things "belong together", similar to clustering. Clustering works by looking
at features of individual points, and grouping items with similar features together. Association analysis doesn't give
the items any individual features, but clusters on the similarities of the relationships.

Other examples:
- Finding voting patterns (if you vote for A, B, and C, you are likely to vote for D). Transactions are representatives, items are bills with "yea" votes.
- Finding associated medical conditions that may have an underlying root causes. Transactions are patients, items are treatments or symptoms.
- Finding outfits. Transactions are things that were worn together, items are individual pieces of clothing. (This is an interesting problem, as two shirts have more 
in common than a shirt and trousers based on features, but you wouldn't wear two shirts and no trousers).


## References

* Wikipedia has great psuedo-code on the [apriori algorithm](https://en.wikipedia.org/wiki/Apriori_algorithm)
* There is another pip installable package, [apyrori](https://github.com/ymoch/apyori/)