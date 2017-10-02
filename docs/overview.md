# Preference High Level Overview

## Glossary (in context of the Pref Service)
* **Item** - An external reference to something that can be preferenced (artwork, a product, etc). Note: The Pref Service only maintains the external id of the item and no actual data or attributes about the item.
* **User** - An external reference to an individual making a series of preferences. Note: The Pref Service only maintains the external id of the user and no actual data or attributes about the user.
* **Preference** - A simple indicator of a like or dislike of an `Item` by a `User`.
* **Transaction** - The set of one or more Preferences for a given `User` (eg. their "session" or "shopping cart").
* **The Algorithm** - A set of procedures to generate Association Rules (i.e. "recommendations") from existing `Transactions` using minimum confidence and minimum support thresholds. This is manually run and is a fairly slow calculation.
* **Association Rule** - An if/then (antecedent/consequent) pattern representing a "recommendation" composed of lists of preferences with an indicator of confidence.
* **Association Rule Set** - A set of Association Rules generated from the same run of `The Algorithm`. There can be a single default `AssociationRuleSet`
* **Support** - The percent of occurrences of an item or combination of items across all known `Transactions`
* **Confidence** - A percentage representing the likelihood an AssociationRule's antecedent correctly implies the consequent.

## Process Overview
### Preference Collection
Preferences are submitted to the service via REST apis ([endpoint](./rest_api.md#post_preferences)).
A preference is simply the combination of the Item's ID, the User's ID making the preference, and a boolean preference representing a like (True) or dislike (False).
This data (along with timestamps) are persisted to the datastore. The "key" (literally the key name in the ndb persistence) of this preference is a string in the form of `<item_id>:<like_or_dislike>` where item_id is the string id of the `Item` and *like_or_dislike* is an int representation of the like or dislike boolean. (eg. `"1234:1"` or `"1234:0"` for a like and dislike of item 1234)

Additionally, we persist an easily queryable "view" of all the `Items` preferenced and the total preferences on that item.
Similarly, we persist an easily queryable "view" of all the `Users` and their preferenced `Items`. This represents a `Transaction`.

### The Algorithm
Using the 1000 most recently updated `Transactions` and a `min_support` and `min_confidence` threshold as input, the algorithm generates association rules. The actual underlying implementation of the algorithm is a priori ([wiki](https://en.wikipedia.org/wiki/Apriori_algorithm)) and a heavily modified version of [this python library](https://github.com/asaini/Apriori/blob/master/apriori.py) used under the MIT-License.

Note: To save on memory and processing time, the `k` value in the a priori algorithm is limited to 5, meaning the set of of all possible combinations of items is limited to a size of 5 items per combination.

Upon the start of each run of the algorithm (aka "`AssociationRule Set` Generation"), an `AssociationRuleSet` is persisted along with the `min_support` and `min_confidence` inputs.

Upon successful completion of the algorithm, a new collection of AssociationRules will be generated with a reference to the parent AssociationRuleSet. Additionally, the parent AssociationRuleSet is updated with the total # of rules generated.

### Making a Recommendations
Generated `AssociationRules` are user independent and in the form of `antecedent => consequent`. Both the antecedent and  consequent are lists of preference keys in the form of `<item_id>:<like_or_dislike>` (see above).
Additionally, the `AssocationRule` has a confidence rating between 0 and .1.
There are two approaches to dealing with Association Rules to make a recommendation:

**User/Transaction Agnostic - Random Recommendation**
In the simplest form, the first `AssociationRule` returned when sorted by confidence in descending order can be returned as the recommendation. Alternately, the rules can be sorted into confidence buckets and random ones can be selected from different confidence buckets. This aids in reinforcing rules that have low confidence upon a successful rule. This is also the best approach when a user doesn't have any previous `Transaction` history.

**User/Transaction Centric**
As the User starts building a `Transaction` history, you can use their transaction data to iteratively find a antecedent with the highest confidence. Since antecedents are lists of pref keys, you can generate your own set of pref keys and find the rules with matches and then order by most matches and highest confidence.

Note: If the `User` already has a `Transaction` history, then it is up to you to decide if you want to use an `AssocationRule` with a consequent containing an item they have already preferenced (e.g. an item they've already purchased or artwork they've already seen).
Similarly, it is up to you to decide if an `Item` in the consequent is available for recommendation (eg. item is in stock, removed from view, etc).



